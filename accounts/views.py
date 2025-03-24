from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.utils import timezone
from django.conf import settings
from .models import User, Certificate
from .forms import SignUpForm, UserProfileForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import re
import os
import json

def validate_password(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long")
    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter")
    if not re.search(r"\d", password):
        raise ValidationError("Password must contain at least one number")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValidationError("Password must contain at least one special character")

@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == 'POST':
        try:
            form = SignUpForm(request.POST)
            if form.is_valid():
                # Validate email format
                try:
                    validate_email(form.cleaned_data['email'])
                except ValidationError:
                    messages.error(request, "Please enter a valid email address.")
                    return render(request, 'accounts/signup.html', {'form': form})

                # Validate password strength
                try:
                    validate_password(form.cleaned_data['password1'])
                except ValidationError as e:
                    messages.error(request, str(e))
                    return render(request, 'accounts/signup.html', {'form': form})

                # Check if email is already registered
                if User.objects.filter(email=form.cleaned_data['email']).exists():
                    messages.error(request, "This email is already registered.")
                    return render(request, 'accounts/signup.html', {'form': form})

                # Create user
                user = form.save(commit=False)
                user.is_active = False
                user.save()

                # Generate token and send verification email
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                verification_url = request.build_absolute_uri(
                    f'/verify-email/{uid}/{token}/'
                )

                # Store verification token in Redis with 24-hour expiry
                cache_key = f'email_verification_{user.email}'
                cache.set(cache_key, token, timeout=86400)  # 24 hours

                # Send verification email
                subject = 'Verify your email address'
                message = render_to_string('accounts/email/verify_email.html', {
                    'user': user,
                    'verification_url': verification_url,
                })
                try:
                    send_mail(
                        subject,
                        message,
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False,
                    )
                    messages.success(request, "Please check your email to verify your account.")
                except Exception as e:
                    messages.error(request, "Failed to send verification email. Please try again later.")
                    user.delete()
                    return render(request, 'accounts/signup.html', {'form': form})

                return redirect('signin')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        except Exception as e:
            messages.error(request, "An unexpected error occurred. Please try again.")
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

@require_http_methods(["GET", "POST"])
def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            # Check if user exists
            if not User.objects.filter(email=email).exists():
                messages.error(request, "No account found with this email address.")
                return render(request, 'accounts/signin.html')

            user = User.objects.get(email=email)
            
            # Check if account is locked
            if user.is_active == False:
                messages.error(request, "Please verify your email address before signing in.")
                return render(request, 'accounts/signin.html')

            # Check login attempts
            login_attempts_key = f'login_attempts_{email}'
            login_attempts = cache.get(login_attempts_key, 0)
            
            if login_attempts >= settings.ACCOUNT_LOGIN_ATTEMPTS_LIMIT:
                messages.error(request, "Too many failed attempts. Please try again later.")
                return render(request, 'accounts/signin.html')

            # Authenticate user
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                # Reset login attempts on successful login
                cache.delete(login_attempts_key)
                login(request, user)
                messages.success(request, "Successfully signed in!")
                return redirect('home')
            else:
                # Increment failed login attempts
                cache.set(login_attempts_key, login_attempts + 1, timeout=settings.ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT)
                messages.error(request, "Invalid password. Please try again.")
                
        except Exception as e:
            messages.error(request, "An error occurred during sign in. Please try again.")
            
    return render(request, 'accounts/signin.html')

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        # Verify token from Redis
        cache_key = f'email_verification_{user.email}'
        stored_token = cache.get(cache_key)
        
        if stored_token and stored_token == token:
            user.is_active = True
            user.save()
            cache.delete(cache_key)
            messages.success(request, "Email verified successfully. You can now sign in.")
            return redirect('signin')
        else:
            messages.error(request, "Invalid or expired verification link.")
            return redirect('signup')
            
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Invalid verification link.")
        return redirect('signup')

@login_required
def home(request):
    return render(request, 'home/index.html')

def logout(request):
    messages.success(request, "Successfully logged out!")
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            # Handle theme preference update
            theme = request.POST.get('theme_preference')
            if theme in ['light', 'dark']:
                user.theme_preference = theme
                user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=request.user)

    # Calculate profile completion percentage
    required_fields = ['first_name', 'last_name', 'email', 'college', 'branch', 'year_of_study']
    filled_fields = sum(1 for field in required_fields if getattr(request.user, field))
    completion_percentage = (filled_fields / len(required_fields)) * 100

    # Get ATS score if resume exists
    ats_score = None
    if request.user.resume:
        ats_score = calculate_ats_score(request.user.resume)

    context = {
        'form': form,
        'completion_percentage': completion_percentage,
        'ats_score': ats_score,
        'certificates': Certificate.objects.filter(user=request.user)
    }
    return render(request, 'dashboard/profile.html', context)

@login_required
def upload_resume(request):
    if request.method == 'POST' and request.FILES.get('resume'):
        resume = request.FILES['resume']
        if resume.size > 5 * 1024 * 1024:  # 5MB limit
            messages.error(request, 'Resume file size must be less than 5MB.')
            return redirect('profile')

        # Delete old resume if exists
        if request.user.resume:
            try:
                os.remove(request.user.resume.path)
            except:
                pass

        # Save new resume
        filename = f'resumes/{request.user.id}/{resume.name}'
        path = default_storage.save(filename, ContentFile(resume.read()))
        request.user.resume = path
        request.user.save()

        messages.success(request, 'Resume uploaded successfully!')
    return redirect('profile')

@login_required
def add_certificate(request):
    if request.method == 'POST' and request.FILES.get('certificate_file'):
        certificate_file = request.FILES['certificate_file']
        if certificate_file.size > 5 * 1024 * 1024:  # 5MB limit
            messages.error(request, 'Certificate file size must be less than 5MB.')
            return redirect('profile')

        Certificate.objects.create(
            user=request.user,
            name=request.POST.get('certificate_name'),
            issuing_organization=request.POST.get('issuing_organization'),
            issue_date=request.POST.get('issue_date'),
            file=certificate_file
        )

        messages.success(request, 'Certificate added successfully!')
    return redirect('profile')

@login_required
@require_http_methods(["POST"])
def update_theme(request):
    try:
        data = json.loads(request.body)
        theme = data.get('theme')
        
        if theme in ['light', 'dark']:
            request.user.theme_preference = theme
            request.user.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid theme'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
