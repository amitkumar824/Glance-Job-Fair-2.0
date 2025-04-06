from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.models import User, Certificate
from accounts.forms import SignUpForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home/index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        course = request.POST.get('course')
        year = request.POST.get('year')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('signup')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                course=course,
                year=year,
                gender=gender,
                phone_number=phone_number
            )
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('signup')

    return render(request, 'home/signup.html')

def signin(request):
    if request.method == 'POST':
        login_id = request.POST.get('login_id')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        try:
            user = User.objects.get(username=login_id)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=login_id)
            except User.DoesNotExist:
                messages.error(request, 'Invalid username or email!')
                return redirect('signin')

        if user.check_password(password):
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            messages.success(request, 'Logged in successfully!')
            return redirect('dashboard_home')
        else:
            messages.error(request, 'Invalid password!')
            return redirect('signin')

    return render(request, 'home/signin.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    return render(request, 'home/contact.html')

def signout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

