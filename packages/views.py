import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Package

stripe.api_key = settings.STRIPE_SECRET_KEY

def packages(request):
    packages = Package.objects.filter(is_active=True)
    return render(request, 'packages/packages.html', {'packages': packages})

@login_required
def checkout(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': package.stripe_price_id,
            'quantity': 1,
        }],
        mode='payment',
        customer_email=request.user.email,
        success_url=request.build_absolute_uri('/packages/success/'),
        cancel_url=request.build_absolute_uri('/packages/'),
        metadata={
            'package_id': package.id,
            'user_id': request.user.id,
        }
    )

    return redirect(checkout_session.url, code=303)

def success(request):
    return render(request, 'packages/success.html')