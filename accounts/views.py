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

from .models import Student, Recruiter, Administrator, Volunteer
from student.models import Job

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
            profile = Student.objects.create(
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
            profile = Recruiter.objects.create(
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
            profile = Administrator.objects.create(
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
            profile = Volunteer.objects.create(
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

