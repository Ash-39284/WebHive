from django.urls import path
from . import views

urlpatterns = [
    path('packages/', views.packages, name='packages'),
    path('packages/checkout/<int:package_id>/', views.checkout, name='checkout'),
    path('packages/success/', views.success, name='payment_success'),
    path('packages/webhook/', views.stripe_webhook, name='stripe_webhook'),
]