from django.db import models
from accounts.models import BaseProfile, Student, Recruiter
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.utils import timezone

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
