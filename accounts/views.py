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

from .models import Student, Recruiter, Administrator, Volunteer

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        phone = request.POST.get('phone')
        whatsapp = request.POST.get('whatsapp')
        location = request.POST.get('location')
        
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
            location=location,
            is_active=False  # User will be activated after email verification
        )
        
        # Send verification email
        send_verification_email(student, request)
        messages.success(request, 'Please check your email to verify your account.')
        return redirect('signin')
        
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
                return redirect('student:dashboard')
            elif hasattr(user, 'recruiter'):
                return redirect('recruiter:dashboard')
            elif hasattr(user, 'administrator'):
                return redirect('administrator:dashboard')
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
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')



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

