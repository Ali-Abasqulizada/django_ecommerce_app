from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .models import Order
import stripe

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    if request.method == 'GET':
        return redirect('core:cart')
    total = request.POST.get('total_cost', '0.00')
    elements = request.POST.get('all_elements')
    counts = request.POST.get('all_elements_counts')
    elements = elements.split(',')
    counts = counts.split(',')
    all_elements = ''
    for i in range(len(elements)):
        row = f'{i + 1}) Product:{elements[i]}, Quantity:{counts[i]}\n'
        all_elements += row
    if total == '0.00':
        return redirect('core:cart')
    context = {
        'elements': all_elements,
        'total': total,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, 'payment/checkout.html', context=context)

def pay(request):
    if request.method == 'GET':
        return redirect('core:cart')
    stripe_token = request.POST.get('stripeToken')
    total = request.POST.get('totalPrice')
    amounts_in_cents = int(float(total) * 100)
    elements = request.POST.get('all_elements')
    try:
        stripe.Charge.create(
            amount=amounts_in_cents,
            currency='usd',
            description=request.user.email,
            source=stripe_token,
        )
        Order.objects.create(
            user=request.user,
            products=elements,
            price=total,
            status='pending'
        )
    except:
        messages.warning(request, 'An error occured')
        return redirect('core:cart')
    messages.success(request, 'Payment Successful')
    return redirect('core:index')