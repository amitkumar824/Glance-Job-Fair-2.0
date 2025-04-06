from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='student_home'),
    path('dashboard/', views.dashboard, name='student_dashboard'),
    path('settings/', views.settings, name='student_settings'),
    # Company uploads URLs
    path('uploads/', views.view_company_uploads, name='view_company_uploads'),
    path('uploads/<int:upload_id>/', views.company_upload_detail, name='company_upload_detail'),
]
