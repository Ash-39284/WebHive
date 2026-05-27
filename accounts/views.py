from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Renders the homepage
def home(request):
    return render(request, 'home.html')

# Handles user login — looks up user by email, authenticates,
# logs them in and redirects to home. Shows error on failure.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Django auth uses username internally, so we look up by email first
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'accounts/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'accounts/register.html')

def logout_view(request):
    logout(request)
    return redirect('home')