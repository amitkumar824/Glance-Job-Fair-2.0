from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Student, Recruiter, Administrator, Volunteer

class BaseProfileInline(admin.StackedInline):
    model = None  # Will be set by child classes
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class StudentInline(BaseProfileInline):
    model = Student
    fieldsets = (
        ('Personal Information', {
            'fields': ('phone', 'whatsapp', 'location', 'profile_picture', 'gender')
        }),
        ('Academic Information', {
            'fields': ('high_school', 'current_year', 'graduation_year', 'is_final_year')
        }),
        ('Professional Information', {
            'fields': ('internship_details', 'cg_profile', 'linkedin_profile', 'github_profile')
        }),
        ('Additional Information', {
            'fields': ('active_backlog', 'total_backlog', 'password_year', 'resume')
        }),
    )

class RecruiterInline(BaseProfileInline):
    model = Recruiter
    fieldsets = (
        ('Personal Information', {
            'fields': ('phone', 'whatsapp', 'location', 'profile_picture')
        }),
        ('Company Information', {
            'fields': ('company_name', 'company_description', 'company_website', 'company_email', 'company_logo')
        }),
    )

class AdministratorInline(BaseProfileInline):
    model = Administrator
    fieldsets = (
        ('Personal Information', {
            'fields': ('phone', 'whatsapp', 'location', 'profile_picture')
        }),
        ('Administrative Information', {
            'fields': ('responsibilities', 'skills', 'departments')
        }),
        ('Additional Information', {
            'fields': ('company_interactions', 'registration_tracking', 'opening_deadlines', 'interview_coordination')
        }),
    )

class VolunteerInline(BaseProfileInline):
    model = Volunteer
    fieldsets = (
        ('Personal Information', {
            'fields': ('phone', 'whatsapp', 'location', 'profile_picture')
        }),
        ('Volunteer Information', {
            'fields': ('responsibilities', 'skills', 'departments')
        }),
        ('Additional Information', {
            'fields': ('event_management', 'support_roles')
        }),
    )

class CustomUserAdmin(UserAdmin):
    inlines = []
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    list_per_page = 25

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        if hasattr(obj, 'student'):
            self.inlines = [StudentInline]
        elif hasattr(obj, 'recruiter'):
            self.inlines = [RecruiterInline]
        elif hasattr(obj, 'administrator'):
            self.inlines = [AdministratorInline]
        elif hasattr(obj, 'volunteer'):
            self.inlines = [VolunteerInline]
        return super().get_inline_instances(request, obj)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register profile models directly for better admin interface
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_year', 'graduation_year', 'is_final_year')
    list_filter = ('current_year', 'graduation_year', 'is_final_year', 'gender')
    search_fields = ('user__username', 'user__email', 'high_school')
    raw_id_fields = ('user',)
    list_per_page = 25

@admin.register(Recruiter)
class RecruiterAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'company_email')
    list_filter = ('company_name',)
    search_fields = ('user__username', 'user__email', 'company_name', 'company_description')
    raw_id_fields = ('user',)
    list_per_page = 25

@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    list_display = ('user', 'departments')
    list_filter = ('departments',)
    search_fields = ('user__username', 'user__email', 'departments', 'responsibilities')
    raw_id_fields = ('user',)
    list_per_page = 25

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('user', 'departments')
    list_filter = ('departments',)
    search_fields = ('user__username', 'user__email', 'departments', 'responsibilities')
    raw_id_fields = ('user',)
    list_per_page = 25
