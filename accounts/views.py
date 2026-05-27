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

# Handles new user registration — validates email and password,
# creates the user, logs them in and redirects to home.
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')

        # Check email isn't already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'accounts/register.html')

        # Enforce minimum password length
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return render(request, 'accounts/register.html')

        # Creates user and log them in immediately
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1
        )
        login(request, user)
        messages.success(request, 'Account created successfully. Welcome!')
        return redirect('home')

    return render(request, 'accounts/register.html')

# Logs the user out and redirects to home
def logout_view(request):
    logout(request)
    return redirect('home')