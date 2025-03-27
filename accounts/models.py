from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class BaseProfile(User):
    phone = models.CharField(max_length=15, blank=True, null=True)
    whatsapp = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        blank=True,
        null=True
    )

    class Meta:
        abstract = True

class StudentProfile(BaseProfile):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

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

    def __str__(self):
        return f"{self.user.username}'s Student Profile"

class RecruiterProfile(BaseProfile):
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

class JobPosting(models.Model):
    JOB_TYPE_CHOICES = [
        ('FT', 'Full-time'),
        ('PT', 'Part-time'),
        ('RM', 'Remote'),
        ('HY', 'Hybrid'),
        ('IO', 'In-office'),
    ]

    INTERVIEW_MODE_CHOICES = [
        ('ON', 'Online'),
        ('OF', 'Offline'),
        ('CP', 'CPN'),
    ]

    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE, related_name='job_postings')
    title = models.CharField(max_length=200)
    job_type = models.CharField(max_length=2, choices=JOB_TYPE_CHOICES)
    job_mode = models.CharField(max_length=2, choices=JOB_TYPE_CHOICES)
    salary_range = models.CharField(max_length=100)
    description = models.TextField()
    internship_details = models.TextField(blank=True, null=True)
    interview_mode = models.CharField(max_length=2, choices=INTERVIEW_MODE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} at {self.recruiter.company_name}"

class AdministratorProfile(BaseProfile):
    responsibilities = models.TextField()
    skills = models.TextField()
    departments = models.TextField()
    company_interactions = models.TextField(blank=True, null=True)
    registration_tracking = models.TextField(blank=True, null=True)
    opening_deadlines = models.TextField(blank=True, null=True)
    interview_coordination = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Administrator Profile"

class VolunteerProfile(BaseProfile):
    responsibilities = models.TextField()
    skills = models.TextField()
    departments = models.TextField()
    event_management = models.TextField(blank=True, null=True)
    support_roles = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Volunteer Profile"

# Signals for profile creation
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # The profile type will be determined during registration
        pass

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        # Try to get any type of profile
        instance.profile.save()
    except:
        pass
