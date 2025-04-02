from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# ============================= Home =======================

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
    return render(request, 'student/index.html', context)

# @login_required
def companies(request):
    """View for browsing available companies and job listings."""
    context = {
        'companies': []  # Will be replaced with actual companies data
    }
    return render(request, 'student/companies.html', context)

# @login_required
def applications(request):
    """View for managing student's job applications."""
    context = {
        'applications': []  # Will be replaced with actual applications data
    }
    return render(request, 'student/applications.html', context)

# @login_required
def notifications(request):
    """View for displaying user notifications."""
    context = {
        'notifications': []  # Will be replaced with actual notifications data
    }
    return render(request, 'student/notifications.html', context)

# @login_required
def profile(request):
    """View for user profile."""
    # Calculate profile completion percentage (placeholder)
    profile_completion = 75
    
    context = {
        'profile_completion': profile_completion,
    }
    return render(request, 'student/profile.html', context)

# @login_required
def settings_view(request):
    """View for user settings."""
    context = {}
    return render(request, 'student/settings.html', context)
