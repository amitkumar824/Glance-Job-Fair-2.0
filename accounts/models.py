from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator


class Student(User):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    phone = models.CharField(max_length=15, blank=True, null=True)
    whatsapp = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        blank=True,
        null=True
    )

    high_school = models.CharField(max_length=200)
    current_year = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        help_text="Current academic year (1-4)"
    )
    graduation_year = models.IntegerField(
        validators=[MinValueValidator(2024), MaxValueValidator(2030)]
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    internship_details = models.TextField(blank=True, null=True)
    cg_profile = models.TextField(blank=True, null=True)
    is_final_year = models.BooleanField(default=False)
    
    # Optional fields
    linkedin_profile = models.URLField(blank=True, null=True)
    github_profile = models.URLField(blank=True, null=True)
    google_certificate = models.FileField(
        upload_to='certificates/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])],
        blank=True,
        null=True
    )
    active_backlog = models.IntegerField(default=0)
    total_backlog = models.IntegerField(default=0)
    password_year = models.IntegerField(blank=True, null=True)
    resume = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])],
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name_plural = "Students"
        ordering = ['username']

    def __str__(self):
        return f"{self.username}'s Student Profile"

class Administrator(User):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        blank=True,
        null=True
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    class Meta:
        verbose_name = "Administrator"
        verbose_name_plural = "Administrators"
        ordering = ['username']

    def __str__(self):
        return f"{self.username}'s Administrator Profile"


class Recruiter(User):
    company_name = models.CharField(max_length=200)
    company_description = models.TextField()
    company_website = models.URLField()
    company_email = models.EmailField()
    company_logo = models.ImageField(
        upload_to='company_logos/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.company_name} - Recruiter Profile"


class Volunteer(User):
    responsibilities = models.TextField()
    skills = models.TextField()
    departments = models.TextField()
    event_management = models.TextField(blank=True, null=True)
    support_roles = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Volunteer Profile"
=======
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
import os

# Custom User Manager for our User model
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, username, password, **extra_fields)

# Custom User model
class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    COURSE_CHOICES = (
        ('BTECH', 'B.Tech'),
        ('MTECH', 'M.Tech'),
        ('BCA', 'BCA'),
        ('MCA', 'MCA'),
    )
    
    email = models.EmailField(unique=True, max_length=50)
    username = models.CharField(unique=True, max_length=50)
    
    # Personal Information
    full_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    
    # Academic Information
    college = models.CharField(max_length=200, blank=True)
    current_year = models.IntegerField(choices=[(i, f'{i}th Year') for i in range(1, 5)], null=True, blank=True)
    course = models.CharField(max_length=10, choices=COURSE_CHOICES, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    total_backlogs = models.IntegerField(default=0)
    current_backlogs = models.IntegerField(default=0)
    
    # Professional Links
    github_profile = models.URLField(blank=True)
    linkedin_profile = models.URLField(blank=True)
    
    # Additional Information
    high_school_info = models.TextField(blank=True)
    internship_details = models.TextField(blank=True)
    
    # Profile Picture and Resume
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    
    # Status Fields
    is_placed = models.BooleanField(default=False)
    is_shortlisted = models.BooleanField(default=False)
    is_btech = models.BooleanField(default=False)
    
    theme_preference = models.CharField(
        max_length=10,
        choices=[
            ('light', 'Light'),
            ('dark', 'Dark'),
        ],
        default='light'
    )
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Set is_btech based on course
        self.is_btech = self.course == 'BTECH'
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete profile picture and resume files
        if self.profile_picture:
            try:
                os.remove(self.profile_picture.path)
            except:
                pass
        if self.resume:
            try:
                os.remove(self.resume.path)
            except:
                pass
        super().delete(*args, **kwargs)

class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    name = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=255)
    issue_date = models.DateField()
    file = models.FileField(upload_to='certificates/%Y/%m/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.name} - {self.issuing_organization}"

    def delete(self, *args, **kwargs):
        # Delete the file when the certificate is deleted
        if self.file:
            try:
                os.remove(self.file.path)
            except:
                pass
        super().delete(*args, **kwargs)
>>>>>>> 1687bb20997a2c7c07f6827d1b8042b382a0a73d
