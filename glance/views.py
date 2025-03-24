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

@login_required
def dashboard_home(request):
    """Dashboard home view showing overview of student's profile and opportunities."""
    context = {
        'job_count': 15,  # Placeholder, replace with actual job count
        'application_count': 3,  # Placeholder, replace with actual application count
        'upcoming_events': [
            {'name': 'Resume Workshop', 'date': '2023-04-15', 'location': 'Online'},
            {'name': 'Mock Interview Session', 'date': '2023-04-20', 'location': 'Hall 3'},
        ],
        'notifications': [
            {'title': 'Profile Review', 'message': 'Your profile has been reviewed by the placement cell.', 'time': '2 hours ago'},
            {'title': 'New Job Opening', 'message': 'A new job opportunity from Microsoft is available.', 'time': '1 day ago'},
        ]
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def companies(request):
    """View for browsing available companies and job listings."""
    context = {
        'companies': []  # Will be replaced with actual companies data
    }
    return render(request, 'dashboard/companies.html', context)

@login_required
def applications(request):
    """View for managing student's job applications."""
    context = {
        'applications': []  # Will be replaced with actual applications data
    }
    return render(request, 'dashboard/applications.html', context)

@login_required
def notifications(request):
    """View for displaying user notifications."""
    context = {
        'notifications': []  # Will be replaced with actual notifications data
    }
    return render(request, 'dashboard/notifications.html', context)

@login_required
def settings_view(request):
    """View for user settings."""
    context = {}
    return render(request, 'dashboard/settings.html', context)
