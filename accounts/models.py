from django.db import models
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
