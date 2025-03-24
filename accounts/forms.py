from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=50, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'full_name', 'phone', 'gender', 'college', 'current_year',
            'course', 'specialization', 'cgpa', 'total_backlogs',
            'current_backlogs', 'github_profile', 'linkedin_profile',
            'high_school_info', 'internship_details'
        ]
        widgets = {
            'high_school_info': forms.Textarea(attrs={'rows': 3}),
            'internship_details': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError('Phone number must contain only digits.')
        return phone

    def clean_cgpa(self):
        cgpa = self.cleaned_data.get('cgpa')
        if cgpa is not None and (cgpa < 0 or cgpa > 10):
            raise forms.ValidationError('CGPA must be between 0 and 10.')
        return cgpa

    def clean_total_backlogs(self):
        total = self.cleaned_data.get('total_backlogs')
        if total is not None and total < 0:
            raise forms.ValidationError('Total backlogs cannot be negative.')
        return total

    def clean_current_backlogs(self):
        current = self.cleaned_data.get('current_backlogs')
        total = self.cleaned_data.get('total_backlogs')
        if current is not None:
            if current < 0:
                raise forms.ValidationError('Current backlogs cannot be negative.')
            if total is not None and current > total:
                raise forms.ValidationError('Current backlogs cannot be more than total backlogs.')
        return current 