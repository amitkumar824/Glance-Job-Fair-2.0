from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.contrib import messages
from .models import CompanyUpload

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

@login_required
def view_company_uploads(request):
    """View for students to see company uploads accessible to them"""
    if not hasattr(request.user, 'student'):
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    
    # Get the student
    student = request.user.student
    
    # Get public uploads and uploads targeted to this student
    public_uploads = CompanyUpload.objects.filter(is_public=True).order_by('-uploaded_at')
    targeted_uploads = CompanyUpload.objects.filter(
        is_public=False, 
        target_students=student
    ).order_by('-uploaded_at')
    
    # Combine the querysets
    all_uploads = public_uploads | targeted_uploads
    all_uploads = all_uploads.distinct().order_by('-uploaded_at')
    
    # Pagination: 12 uploads per page
    paginator = Paginator(all_uploads, 12)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.get_page(1)
    
    # Group uploads by type
    jd_uploads = all_uploads.filter(upload_type='JD')[:5]
    brochures = all_uploads.filter(upload_type='BR')[:5]
    presentations = all_uploads.filter(upload_type='PR')[:5]
    videos = all_uploads.filter(upload_type='VD')[:5]
    other_uploads = all_uploads.filter(upload_type='OT')[:5]
    
    context = {
        'uploads': page_obj,
        'jd_uploads': jd_uploads,
        'brochures': brochures,
        'presentations': presentations,
        'videos': videos,
        'other_uploads': other_uploads,
        'total_uploads': all_uploads.count(),
    }
    
    return render(request, 'student/company_uploads.html', context)

@login_required
def company_upload_detail(request, upload_id):
    """View for students to see details of a specific company upload"""
    if not hasattr(request.user, 'student'):
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    
    # Get the student
    student = request.user.student
    
    try:
        # Check if the upload is accessible to this student
        upload = CompanyUpload.objects.get(
            Q(is_public=True) | Q(is_public=False, target_students=student),
            id=upload_id
        )
        
        # Get more uploads from the same company
        more_from_company = CompanyUpload.objects.filter(
            Q(is_public=True) | Q(is_public=False, target_students=student),
            company=upload.company
        ).exclude(id=upload.id)[:4]
        
        # Get more uploads of the same type
        more_of_same_type = CompanyUpload.objects.filter(
            Q(is_public=True) | Q(is_public=False, target_students=student),
            upload_type=upload.upload_type
        ).exclude(id=upload.id)[:4]
        
        context = {
            'upload': upload,
            'more_from_company': more_from_company,
            'more_of_same_type': more_of_same_type,
        }
        
        return render(request, 'student/company_upload_detail.html', context)
    
    except CompanyUpload.DoesNotExist:
        messages.error(request, 'The requested upload does not exist or you do not have access to it.')
        return redirect('view_company_uploads')
