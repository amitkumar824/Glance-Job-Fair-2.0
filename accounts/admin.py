from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Add custom fields to fieldsets
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'course', 'year', 'gender', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # Add custom fields to add_fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'course', 'year', 'gender', 'password1', 'password2'),
        }),
    )
    # Add custom fields to list_display
    list_display = ('username', 'email', 'course', 'year', 'gender', 'is_staff')
    # Add custom fields to search_fields
    search_fields = ('username', 'email', 'course')
    # Add custom fields to list_filter
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'gender', 'year')

# Register custom User model
admin.site.register(User, CustomUserAdmin)
