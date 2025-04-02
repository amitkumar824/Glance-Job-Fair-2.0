from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
<<<<<<< HEAD
from django.contrib.auth.models import User
from .models import Student, Recruiter, Administrator, Volunteer

# Register profile models directly for better admin interface
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'current_year', 'graduation_year', 'is_final_year')
    list_filter = ('current_year', 'graduation_year', 'is_final_year', 'gender')
    exclude = ('password', 'groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login')
    search_fields = ('username', 'email', 'high_school')
    list_per_page = 25

@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    list_display = ('username', "first_name", "last_name")
    exclude = ('password', 'groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login')
=======
from .models import User, Certificate

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'full_name', 'current_year', 'course', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'course', 'current_year', 'gender')
    search_fields = ('username', 'email', 'full_name', 'college')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Information', {'fields': ('full_name', 'phone', 'gender', 'profile_picture')}),
        ('Academic Information', {'fields': ('college', 'current_year', 'course', 'specialization', 'cgpa', 'total_backlogs', 'current_backlogs')}),
        ('Professional Links', {'fields': ('github_profile', 'linkedin_profile')}),
        ('Additional Information', {'fields': ('high_school_info', 'internship_details', 'resume')}),
        ('Status', {'fields': ('is_placed', 'is_shortlisted', 'is_btech')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

# Register custom User model
admin.site.register(User, CustomUserAdmin)
admin.site.register(Certificate)
>>>>>>> 1687bb20997a2c7c07f6827d1b8042b382a0a73d
