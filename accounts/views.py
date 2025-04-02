from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .models import Student, Recruiter, Administrator, Volunteer

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        phone = request.POST.get('phone')
        whatsapp = request.POST.get('whatsapp')
        current_year = request.POST.get("current_year")
        graduation_year = request.POST.get("graduation_year")
        high_school = request.POST.get("high_school")
        gender = request.POST.get("gender")
        
        profile_picture = request.FILES.get("profile_picture")
        
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
        student = Student.objects.create(
            username=username,
            email=email,
            password=password1,
            phone=phone,
            whatsapp=whatsapp,
            current_year = current_year,
            graduation_year = graduation_year,
            high_school = high_school,
            gender = gender,
            profile_picture = profile_picture,
            is_active=False  # User will be activated after email verification
        )
        
        student.set_password(password1)
        
        student.save()
        # Send verification email
        send_verification_email(student, request)
        messages.success(request, 'Please check your email to verify your account.')
        return redirect('login')
        
    return render(request, 'accounts/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Check user role and redirect accordingly
            if hasattr(user, 'student'):
                return redirect('dashboard')
            elif hasattr(user, 'administrator'):
                return redirect('administrator')
            elif hasattr(user, 'recruiter'):
                return redirect('recruiter:dashboard')
            elif hasattr(user, 'volunteer'):
                return redirect('volunteer:dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def send_verification_email(user, request):
    print("sending email")
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_url = request.build_absolute_uri(f'/accounts/verify-email/{uid}/{token}/')
    
    subject = 'Verify your email address'
    message = render_to_string('accounts/email/verify_email.html', {
        'user': user,
        'verification_url': verification_url,
    })
    #17
    #
    send_mail(
        subject,
        strip_tags(message),
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
        html_message=message
    )
    
    print("email sent")

def verify_email(request, token):
    try:
        user = User.objects.get(verification_token=token)
        if not user.is_active:
            user.is_active = True
            user.save()
            messages.success(request, 'Email verified successfully! You can now log in.')
        else:
            messages.info(request, 'Email already verified. You can log in.')
        return redirect('signin')
    except User.DoesNotExist:
        messages.error(request, 'Invalid verification token.')
        return redirect('signup')

@login_required
@require_POST
def update_theme(request):
    """Update user's theme preference."""
    try:
        data = json.loads(request.body)
        theme = data.get('theme')
        
        if theme not in ['light', 'dark']:
            return JsonResponse({'success': False, 'error': 'Invalid theme'}, status=400)
            
        request.user.student.theme_preference = theme
        request.user.student.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
