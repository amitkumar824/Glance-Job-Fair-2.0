from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError, PermissionDenied
from django.conf import settings
from .models import Student
from django.contrib.auth.models import User
import os

# Create your views here.

@login_required
def dashboard(request):
    if not hasattr(request.user, 'student'):
        raise PermissionDenied("This page is only accessible to students.")
    
    
    return render(request, 'student/dashboard.html')

@login_required
def profile(request):
    if not hasattr(request.user, 'student'):
        raise PermissionDenied("This page is only accessible to students.")

    if request.method == 'POST':
        try:
            # Update User model fields
            user = request.user
            full_name = request.POST.get('full_name', '').strip()
            if full_name:
                name_parts = full_name.split()
                user.first_name = name_parts[0]
                user.last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
            
            email = request.POST.get('email', '').strip()
            if email:
                user.email = email
            
            user.save()

            # Update Student model fields
            student = user.student
            
            # Basic Information
            student.phone = request.POST.get('phone', '').strip()
            student.whatsapp = request.POST.get('whatsapp', '').strip()
            student.location = request.POST.get('location', '').strip()
            student.gender = request.POST.get('gender', '').strip()
            
            # Academic Information
            student.high_school = request.POST.get('college', '').strip()
            student.current_year = request.POST.get('current_year', '').strip()
            student.course = request.POST.get('course', '').strip()
            student.specialization = request.POST.get('specialization', '').strip()
            
            # Handle numeric fields
            try:
                student.graduation_year = int(request.POST.get('graduation_year', 0))
            except ValueError:
                student.graduation_year = None
                
            try:
                student.cgpa = float(request.POST.get('cgpa', 0))
            except ValueError:
                student.cgpa = None
                
            try:
                student.active_backlog = int(request.POST.get('active_backlog', 0))
            except ValueError:
                student.active_backlog = 0
                
            try:
                student.total_backlog = int(request.POST.get('total_backlog', 0))
            except ValueError:
                student.total_backlog = 0
            
            # Professional Information
            student.github_profile = request.POST.get('github_profile', '').strip()
            student.linkedin_profile = request.POST.get('linkedin_profile', '').strip()
            student.internship_details = request.POST.get('internship_details', '').strip()
            student.cg_profile = request.POST.get('cg_profile', '').strip()
            
            # Status Information
            student.is_final_year = request.POST.get('is_final_year') == 'on'
            student.is_placed = request.POST.get('is_placed') == 'on'

            # Handle file uploads
            if 'profile_picture' in request.FILES:
                profile_picture = request.FILES['profile_picture']
                # Delete old profile picture if exists
                if student.profile_picture:
                    try:
                        os.remove(student.profile_picture.path)
                    except:
                        pass
                student.profile_picture.save(f'profile_pictures/{user.id}/{profile_picture.name}', profile_picture)

            if 'resume' in request.FILES:
                resume = request.FILES['resume']
                # Delete old resume if exists
                if student.resume:
                    try:
                        os.remove(student.resume.path)
                    except:
                        pass
                student.resume.save(f'resumes/{user.id}/{resume.name}', resume)

            if 'google_certificate' in request.FILES:
                certificate = request.FILES['google_certificate']
                # Delete old certificate if exists
                if student.google_certificate:
                    try:
                        os.remove(student.google_certificate.path)
                    except:
                        pass
                student.google_certificate.save(f'certificates/{user.id}/{certificate.name}', certificate)

            # Validate and save
            student.full_clean()
            student.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('student:profile')

        except ValidationError as e:
            messages.error(request, f'Validation error: {str(e)}')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
        return redirect('student:profile')

    # Calculate profile completion percentage
    completion_percentage = user.student.profile_completion_percentage
    
    context = {
        'completion_percentage': completion_percentage,
    }
    return render(request, 'student/profile.html', context)
=======

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
    return render(request, 'dashboard/index.html', context)

# @login_required
def companies(request):
    """View for browsing available companies and job listings."""
    context = {
        'companies': []  # Will be replaced with actual companies data
    }
    return render(request, 'dashboard/companies.html', context)

# @login_required
def applications(request):
    """View for managing student's job applications."""
    context = {
        'applications': []  # Will be replaced with actual applications data
    }
    return render(request, 'dashboard/applications.html', context)

# @login_required
def notifications(request):
    """View for displaying user notifications."""
    context = {
        'notifications': []  # Will be replaced with actual notifications data
    }
    return render(request, 'dashboard/notifications.html', context)

# @login_required
def profile(request):
    """View for user profile."""
    # Calculate profile completion percentage (placeholder)
    profile_completion = 75
    
    context = {
        'profile_completion': profile_completion,
    }
    return render(request, 'dashboard/profile.html', context)

# @login_required
def settings_view(request):
    """View for user settings."""
    context = {}
    return render(request, 'dashboard/settings.html', context)
>>>>>>> 1687bb20997a2c7c07f6827d1b8042b382a0a73d
