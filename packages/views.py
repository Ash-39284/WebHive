import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Package
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

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

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        package_id = session['metadata']['package_id']
        user_id = session['metadata']['user_id']
        amount = session['amount_total']
        email = session.get('customer_email', '')
        payment_intent = session.get('payment_intent', '')
        customer_id = session.get('customer', '')

        try:
            from django.contrib.auth.models import User
            from accounts.models import UserProfile
            from orders.models import Order, Payment

            user = User.objects.get(id=user_id)
            profile = UserProfile.objects.get(user=user)
            package = Package.objects.get(id=package_id)

            order = Order.objects.create(
                user_profile=profile,
                package=package,
                full_name=user.get_full_name() or email,
                email=email,
                order_total=amount / 100,
                status='paid'
            )

            Payment.objects.create(
                order=order,
                stripe_payment_intent=payment_intent,
                stripe_customer_id=customer_id or '',
                amount=amount / 100,
                currency='gbp',
                status='succeeded'
            )

            print(f'Order {order.id} created for {email}')

        except Exception as e:
            print(f'Webhook error: {e}')

    return HttpResponse(status=200)