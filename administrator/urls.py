from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='administrator'),
    
    # Company URLs
    path('companies/', views.manage_companies, name='manage_companies'),
    path('companies/create/', views.company_create, name='company_create'),
    path('companies/<int:company_id>/', views.company_details, name='company_details'),
    path('companies/<int:company_id>/update/', views.company_update, name='company_update'),
    path('companies/<int:company_id>/delete/', views.company_delete, name='company_delete'),
    
    # Job URLs
    path('jobs/', views.manage_jobs, name='manage_jobs'),
    path('jobs/create/', views.job_create, name='job_create'),
    path('jobs/<int:job_id>/', views.job_details, name='job_details'),
    path('jobs/<int:job_id>/update/', views.job_update, name='job_update'),
    path('jobs/<int:job_id>/delete/', views.job_delete, name='job_delete'),
    
    # Company Upload URLs
    path('uploads/', views.manage_company_uploads, name='manage_company_uploads'),
    path('uploads/create/', views.company_upload_create, name='company_upload_create'),
    path('uploads/<int:upload_id>/', views.company_upload_details, name='company_upload_details'),
    path('uploads/<int:upload_id>/update/', views.company_upload_update, name='company_upload_update'),
    path('uploads/<int:upload_id>/delete/', views.company_upload_delete, name='company_upload_delete'),
]
