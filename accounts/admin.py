from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
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
