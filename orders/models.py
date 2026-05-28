from django.db import models
from accounts.models import UserProfile
from packages.models import Package

class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='orders')
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, related_name='orders')
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=255)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} - {self.email}'


class Payment(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    stripe_payment_intent = models.CharField(max_length=255)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='gbp')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment {self.id} - {self.order.email}'