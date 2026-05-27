from django.shortcuts import render
from .models import Package

def packages(request):
    packages = Package.objects.filter(is_active=True)
    return render(request, 'packages/packages.html', {'packages': packages})

