from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

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
    
    YEAR_CHOICES = (
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
        ('5', '5th Year'),
        ('G', 'Graduate'),
        ('PG', 'Post Graduate'),
    )
    
    email = models.EmailField(unique=True, max_length=50)
    username = models.CharField(unique=True, max_length=50)
    course = models.CharField(max_length=100)
    year = models.CharField(max_length=2, choices=YEAR_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    objects = CustomUserManager()
    
    # Email and username fields are both required for login, but we'll use username as the unique identifier
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'course', 'year', 'gender']
    
    def __str__(self):
        return self.username
