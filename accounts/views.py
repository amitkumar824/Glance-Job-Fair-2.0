from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm,
    StudentProfileForm, RecruiterProfileForm,
    AdministratorProfileForm, VolunteerProfileForm,
    JobPostingForm
)
from .models import StudentProfile, RecruiterProfile, AdministratorProfile, VolunteerProfile, JobPosting

# Create your views here.

def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_url = request.build_absolute_uri(f'/accounts/verify-email/{uid}/{token}/')
    
    subject = 'Verify your email address'
    message = render_to_string('accounts/email/verify_email.html', {
        'user': user,
        'verification_url': verification_url,
    })
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been verified. You can now login.')
        return redirect('signin')
    else:
        messages.error(request, 'Invalid verification link.')
        return redirect('signup')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('signup')
            
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')
            
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            is_active=False  # User will be activated after email verification
        )
        
        # Create profile based on role
        if role == 'student':
            profile = StudentProfile.objects.create(
                user=user,
                phone=request.POST.get('phone'),
                whatsapp=request.POST.get('whatsapp'),
                location=request.POST.get('location'),
                profile_picture=request.FILES.get('profile_picture'),
                high_school=request.POST.get('high_school'),
                current_year=request.POST.get('current_year'),
                graduation_year=request.POST.get('graduation_year'),
                gender=request.POST.get('gender')
            )
        elif role == 'recruiter':
            profile = RecruiterProfile.objects.create(
                user=user,
                phone=request.POST.get('phone'),
                whatsapp=request.POST.get('whatsapp'),
                location=request.POST.get('location'),
                profile_picture=request.FILES.get('profile_picture'),
                company_name=request.POST.get('company_name'),
                company_description=request.POST.get('company_description'),
                company_website=request.POST.get('company_website'),
                company_email=request.POST.get('company_email'),
                company_logo=request.FILES.get('company_logo')
            )
        elif role == 'admin':
            profile = AdministratorProfile.objects.create(
                user=user,
                phone=request.POST.get('phone'),
                whatsapp=request.POST.get('whatsapp'),
                location=request.POST.get('location'),
                profile_picture=request.FILES.get('profile_picture'),
                responsibilities=request.POST.get('responsibilities', ''),
                skills=request.POST.get('skills', ''),
                departments=request.POST.get('departments', '')
            )
        else:  # volunteer
            profile = VolunteerProfile.objects.create(
                user=user,
                phone=request.POST.get('phone'),
                whatsapp=request.POST.get('whatsapp'),
                location=request.POST.get('location'),
                profile_picture=request.FILES.get('profile_picture'),
                responsibilities=request.POST.get('responsibilities', ''),
                skills=request.POST.get('skills', ''),
                departments=request.POST.get('departments', '')
            )
        
        # Send verification email
        send_verification_email(user, request)
        messages.success(request, 'Please check your email to verify your account.')
        return redirect('signin')
        
    return render(request, 'accounts/signup.html')

def signin(request):
    if request.method == 'POST':
        login_id = request.POST.get('login_id')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        # Try to authenticate with username or email
        user = None
        if '@' in login_id:
            try:
                user_obj = User.objects.get(email=login_id)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                messages.error(request, 'No user found with this email address.')
                return redirect('signin')
        else:
            user = authenticate(username=login_id, password=password)
        
        if user is not None:
            if not user.is_active:
                messages.error(request, 'Please verify your email before logging in.')
                return redirect('signin')
                
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)  # Session expires when browser closes
                
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect based on user role
            if hasattr(user, 'studentprofile'):
                return redirect('student_dashboard')
            elif hasattr(user, 'recruiterprofile'):
                return redirect('recruiter_dashboard')
            elif hasattr(user, 'administratorprofile'):
                return redirect('admin_dashboard')
            elif hasattr(user, 'volunteerprofile'):
                return redirect('volunteer_dashboard')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            
    return render(request, 'accounts/signin.html')

@login_required
def profile(request):
    user = request.user
    if not hasattr(user, 'profile'):
        raise PermissionDenied("No profile found for this user.")
    
    profile = user.profile
    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    user = request.user
    if not hasattr(user, 'profile'):
        raise PermissionDenied("No profile found for this user.")
    
    profile = user.profile
    
    if request.method == 'POST':
        # Update user fields
        user.email = request.POST.get('email', user.email)
        user.save()
        
        # Update profile fields
        profile.phone = request.POST.get('phone', profile.phone)
        profile.whatsapp = request.POST.get('whatsapp', profile.whatsapp)
        profile.location = request.POST.get('location', profile.location)
        
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
            
        # Update role-specific fields
        if isinstance(profile, StudentProfile):
            profile.high_school = request.POST.get('high_school', profile.high_school)
            profile.current_year = request.POST.get('current_year', profile.current_year)
            profile.graduation_year = request.POST.get('graduation_year', profile.graduation_year)
            profile.gender = request.POST.get('gender', profile.gender)
        elif isinstance(profile, RecruiterProfile):
            profile.company_name = request.POST.get('company_name', profile.company_name)
            profile.company_description = request.POST.get('company_description', profile.company_description)
            profile.company_website = request.POST.get('company_website', profile.company_website)
            profile.company_email = request.POST.get('company_email', profile.company_email)
            if 'company_logo' in request.FILES:
                profile.company_logo = request.FILES['company_logo']
                
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
        
    return render(request, 'accounts/edit_profile.html', {'profile': profile})

# Job posting views
@login_required
def create_job_posting(request):
    if not isinstance(request.user.profile, RecruiterProfile):
        raise PermissionDenied("Only recruiters can create job postings.")
    
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user.profile
            job.save()
            messages.success(request, 'Job posting created successfully.')
            return redirect('recruiter_dashboard')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = JobPostingForm()
    
    return render(request, 'accounts/create_job_posting.html', {'form': form})

@login_required
def edit_job_posting(request, job_id):
    if not isinstance(request.user.profile, RecruiterProfile):
        raise PermissionDenied("Only recruiters can edit job postings.")
    
    try:
        job = JobPosting.objects.get(id=job_id, recruiter=request.user.profile)
    except JobPosting.DoesNotExist:
        raise PermissionDenied("Job posting not found or you don't have permission to edit it.")
    
    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job posting updated successfully.')
            return redirect('recruiter_dashboard')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = JobPostingForm(instance=job)
    
    return render(request, 'accounts/edit_job_posting.html', {'form': form, 'job': job})
