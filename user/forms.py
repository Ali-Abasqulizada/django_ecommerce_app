from django.contrib.auth.models import User
from django import forms


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        max_length=100,
        label='Username'
    )

    password = forms.CharField(
        max_length=50,
        min_length=3,
        label='Password',
        widget=forms.PasswordInput
    )

    confirm = forms.CharField(
        label='Confirm your password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm')
        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords don't match!")
        return cleaned_data
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username).first()
        if user and not user.is_active:
            user.delete()
        elif user:
            raise forms.ValidationError('User with this username is already exists!')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()
        if user and not user.is_active:
            user.delete()
        elif user:
            raise forms.ValidationError('User with email is already exists!')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email'
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )

class PasswordResetEmailForm(forms.Form):
    email = forms.EmailField(
        label='Email'
    )

class SetNewResetPasswordForm(forms.Form):
    password = forms.CharField(
        max_length=50,
        min_length=3,
        label='New Password',
        widget=forms.PasswordInput
    )

    confirm = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm')
        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords don't match!")
        return cleaned_data