from django.db import models
from accounts.models import Student, Recruiter
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator, URLValidator
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Company(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    website = models.URLField()
    email = models.EmailField()
    location = models.CharField(max_length=200)
    logo = models.ImageField(
        upload_to='company_logos/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['name']

    def __str__(self):
        return self.name

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('FT', 'Full-time'),
        ('PT', 'Part-time'),
        ('IN', 'Internship'),
        ('CT', 'Contract'),
        ('TP', 'Temporary'),
    ]

    JOB_MODE_CHOICES = [
        ('RM', 'Remote'),
        ('HY', 'Hybrid'),
        ('IO', 'In-office'),
        ('FL', 'Flexible'),
    ]

    INTERVIEW_MODE_CHOICES = [
        ('ON', 'Online'),
        ('OF', 'Offline'),
        ('CP', 'CPN'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name='posted_jobs')
    title = models.CharField(max_length=200)
    job_type = models.CharField(max_length=2, choices=JOB_TYPE_CHOICES)
    job_mode = models.CharField(max_length=2, choices=JOB_MODE_CHOICES)
    salary_range = models.CharField(max_length=100)
    description = models.TextField()
    responsibilities = models.TextField()
    required_skills = models.TextField()
    interview_mode = models.CharField(max_length=2, choices=INTERVIEW_MODE_CHOICES)
    interview_date = models.DateTimeField()
    number_of_openings = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    applicants = models.ManyToManyField(Student, through='JobApplication', related_name='applied_jobs', blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['company', 'is_active']),
            models.Index(fields=['recruiter', 'is_active']),
            models.Index(fields=['deadline']),
            models.Index(fields=['interview_date']),
        ]

    def __str__(self):
        return f"{self.title} at {self.company.name}"

    def is_deadline_passed(self):
        return timezone.now() > self.deadline

    def is_interview_passed(self):
        return timezone.now() > self.interview_date

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('PD', 'Pending'),
        ('AC', 'Accepted'),
        ('RJ', 'Rejected'),
        ('WD', 'Withdrawn'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='PD')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ['job', 'student']
        ordering = ['-applied_at']
        indexes = [
            models.Index(fields=['job', 'student']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.student.user.username}'s application for {self.job.title}"

class CompanyUpload(models.Model):
    """Model for company uploads that students can access"""
    UPLOAD_TYPE_CHOICES = [
        ('JD', 'Job Description'),
        ('BR', 'Brochure'),
        ('PR', 'Presentation'),
        ('VD', 'Video'),
        ('OT', 'Other'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='uploads')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    upload_type = models.CharField(max_length=2, choices=UPLOAD_TYPE_CHOICES, default='OT')
    file = models.FileField(upload_to='company_uploads/', blank=True, null=True)
    external_url = models.URLField(blank=True, null=True, 
                                  help_text="For external resources like videos or websites")
    is_public = models.BooleanField(default=True, 
                                   help_text="If unchecked, only specific students can access this")
    target_students = models.ManyToManyField('accounts.Student', blank=True, related_name='company_uploads',
                                            help_text="Specific students who can access this upload")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Company Upload"
        verbose_name_plural = "Company Uploads"

    def __str__(self):
        return f"{self.title} by {self.company.name}"

    def get_absolute_url(self):
        return self.file.url if self.file else self.external_url
