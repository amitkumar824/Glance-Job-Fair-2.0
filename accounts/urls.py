from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/upload-resume/', views.upload_resume, name='upload_resume'),
    path('profile/add-certificate/', views.add_certificate, name='add_certificate'),
    path('update-theme/', views.update_theme, name='update_theme'),
] 