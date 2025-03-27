from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import StudentProfile, RecruiterProfile, AdministratorProfile, VolunteerProfile, JobPosting
import re

class BaseProfileForm(forms.ModelForm):
    class Meta:
        abstract = True
        fields = ['phone', 'whatsapp', 'location', 'profile_picture']

class StudentProfileForm(BaseProfileForm):
    class Meta(BaseProfileForm.Meta):
        model = StudentProfile
        fields = BaseProfileForm.Meta.fields + [
            'high_school', 'current_year', 'graduation_year', 'gender',
            'internship_details', 'cg_profile', 'is_final_year',
            'linkedin_profile', 'github_profile', 'google_certificate',
            'active_backlog', 'total_backlog', 'password_year', 'resume'
        ]
        widgets = {
            'internship_details': forms.Textarea(attrs={'rows': 4}),
            'cg_profile': forms.Textarea(attrs={'rows': 4}),
        }

class RecruiterProfileForm(BaseProfileForm):
    class Meta(BaseProfileForm.Meta):
        model = RecruiterProfile
        fields = BaseProfileForm.Meta.fields + [
            'company_name', 'company_description', 'company_website',
            'company_email', 'company_logo'
        ]
        widgets = {
            'company_description': forms.Textarea(attrs={'rows': 4}),
        }

class AdministratorProfileForm(BaseProfileForm):
    class Meta(BaseProfileForm.Meta):
        model = AdministratorProfile
        fields = BaseProfileForm.Meta.fields + [
            'responsibilities', 'skills', 'departments',
            'company_interactions', 'registration_tracking',
            'opening_deadlines', 'interview_coordination'
        ]
        widgets = {
            'responsibilities': forms.Textarea(attrs={'rows': 4}),
            'skills': forms.Textarea(attrs={'rows': 4}),
            'departments': forms.Textarea(attrs={'rows': 4}),
            'company_interactions': forms.Textarea(attrs={'rows': 4}),
            'registration_tracking': forms.Textarea(attrs={'rows': 4}),
            'opening_deadlines': forms.Textarea(attrs={'rows': 4}),
            'interview_coordination': forms.Textarea(attrs={'rows': 4}),
        }

class VolunteerProfileForm(BaseProfileForm):
    class Meta(BaseProfileForm.Meta):
        model = VolunteerProfile
        fields = BaseProfileForm.Meta.fields + [
            'responsibilities', 'skills', 'departments',
            'event_management', 'support_roles'
        ]
        widgets = {
            'responsibilities': forms.Textarea(attrs={'rows': 4}),
            'skills': forms.Textarea(attrs={'rows': 4}),
            'departments': forms.Textarea(attrs={'rows': 4}),
            'event_management': forms.Textarea(attrs={'rows': 4}),
            'support_roles': forms.Textarea(attrs={'rows': 4}),
        }

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = [
            'title', 'job_type', 'job_mode', 'salary_range',
            'description', 'internship_details', 'interview_mode',
            'deadline'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
            'internship_details': forms.Textarea(attrs={'rows': 4}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('recruiter', 'Recruiter'),
        ('admin', 'Administrator'),
        ('volunteer', 'Volunteer'),
    ]

    email = forms.EmailField(max_length=50, required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 50:
            raise forms.ValidationError('Username must be less than 50 characters.')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'\d', password):
            raise forms.ValidationError('Password must contain at least one number.')
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create or update profile
            profile = user.profile
            profile.role = self.cleaned_data['role']
            profile.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=50,
        label='Email or Username',
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' in username:
            try:
                user = User.objects.get(email=username)
                return user.username  # Return username for authentication
            except User.DoesNotExist:
                raise forms.ValidationError('No user found with this email address.')
        return username 