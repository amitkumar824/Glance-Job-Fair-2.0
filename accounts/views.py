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
    
    try:
        send_mail(
            subject,
            strip_tags(message),
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
            html_message=message
        )
        print(f"Email sent successfully to {user.email}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        # If in development, still allow account to be activated
        if settings.DEBUG:
            print(f"Debug mode: Activating account anyway")
            print(f"Verification URL would have been: {verification_url}")
            user.is_active = True
            user.save()

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        if default_token_generator.check_token(user, token):
            if not user.is_active:
                user.is_active = True
                user.save()
                messages.success(request, 'Email verified successfully! You can now log in.')
            else:
                messages.info(request, 'Email already verified. You can log in.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid verification link.')
            return redirect('signup')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'Invalid verification link.')
        return redirect('signup')

@login_required
def test_email(request):
    # Get email configuration from settings
    email_host = settings.EMAIL_HOST
    email_port = settings.EMAIL_PORT
    email_use_tls = settings.EMAIL_USE_TLS
    email_use_ssl = settings.EMAIL_USE_SSL
    default_from_email = settings.DEFAULT_FROM_EMAIL
    
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                # Create a test email
                subject = 'GLANCE Test Email'
                message = 'This is a test email from GLANCE.'
                html_message = '<h1>Test Email</h1><p>This is a test email from GLANCE.</p>'
                
                # Send the email
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=default_from_email,
                    recipient_list=[email],
                    html_message=html_message,
                    fail_silently=False
                )
                messages.success(request, f'Test email sent to {email}.')
            except Exception as e:
                messages.error(request, f'Failed to send test email: {str(e)}')
                
    # Pass email configuration to the template
    context = {
        'email_host': email_host,
        'email_port': email_port,
        'email_use_tls': email_use_tls,
        'email_use_ssl': email_use_ssl,
        'default_from_email': default_from_email,
    }
    
    return render(request, 'accounts/test_email.html', context)

@login_required
def api_students_list(request):
    """API endpoint to get a list of students for company uploads"""
    if not (request.user.is_staff or hasattr(request.user, 'administrator') or hasattr(request.user, 'recruiter')):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        students = Student.objects.all()
        student_data = []
        
        for student in students:
            student_data.append({
                'id': student.id,
                'username': student.user.username,
                'email': student.user.email,
                'full_name': f"{student.user.first_name} {student.user.last_name}".strip() or student.user.username
            })
        
        return JsonResponse({'students': student_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
