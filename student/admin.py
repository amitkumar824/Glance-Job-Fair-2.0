from django.contrib import admin
from .models import Company, Job, JobApplication

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'email', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description', 'location')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)
    list_per_page = 25

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'job_type', 'job_mode', 'deadline', 'is_active')
    list_filter = ('job_type', 'job_mode', 'interview_mode', 'is_active', 'deadline')
    search_fields = ('title', 'company__name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    list_per_page = 25
    date_hierarchy = 'deadline'
    raw_id_fields = ('company', 'recruiter')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'student', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('job__title', 'student__user__username', 'notes')
    readonly_fields = ('applied_at', 'updated_at')
    ordering = ('-applied_at',)
    list_per_page = 25
    raw_id_fields = ('job', 'student')
