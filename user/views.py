from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from . import forms, tokens

# Create your views here.

def register_user(request):
    if request.user.is_authenticated:
        return redirect('core:index')
    form = forms.RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        context = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': tokens.account_activation_token.make_token(user)
        }
        mail_subject = 'Activate your account'
        mail_body = render_to_string('user/verify_email.html', context=context)
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject,
            mail_body,
            to=[to_email]
        )
        email.content_subtype = 'html'
        email.send()
        messages.info(request, f"We send mail to '{to_email}' gmail account. Please verify that is you")
        return redirect('core:index')
    return render(request, 'user/register.html', {'form':form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and tokens.account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, f'Welcome {user.username}')
        return redirect('core:index')
    messages.error(request, 'Token is invalid or expired')
    return redirect('core:index')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('core:index')
    form = forms.LoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = User.objects.filter(email=email).first()
        if user and user.is_active and user.check_password(password):
            login(request, user)
            messages.success(request, f'Welcome back {user.username}')
            return redirect(request.GET.get('next') or request.POST.get('next') or 'core:index')
        messages.error(request, 'Username or Password is invalid')
    return render(request, 'user/login.html', {'form':form})

def logout_user(request):
    logout(request)
    messages.success(request, 'Bye')
    return redirect('core:index')

def password_reset_email(request):
    if request.user.is_authenticated:
        return redirect('core:index')
    form = forms.PasswordResetEmailForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            current_site = get_current_site(request)
            context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': tokens.password_reset_token.make_token(user)
            }
            mail_subject = 'Reset your password'
            mail_body = render_to_string('user/password_reset_send_email.html', context)
            email_message = EmailMessage(mail_subject, mail_body, to=[email])
            email_message.content_subtype = 'html'
            email_message.send()
            messages.info(request, 'Password reset link sent. Please check your email.')
            return redirect('core:index')
        messages.error(request, f'User with that email does not exist')
    return render(request, 'user/password_reset_email.html', {'form':form})

def set_new_password(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and tokens.password_reset_token.check_token(user, token):
        form = forms.SetNewResetPasswordForm(request.POST or None)
        if form.is_valid():
            new_password = form.cleaned_data.get('password')
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Your password changed successfully!')
            return redirect('user:login')
        return render(request, 'user/set_new_password.html', {'form':form})
    messages.error(request, "Reset link is invalid or expired!")
    return redirect('user:password_reset_email')
