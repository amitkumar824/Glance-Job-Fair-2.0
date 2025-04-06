from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('verify-email/<uuid:token>/', views.verify_email, name='verify_email'),
    path('test-email/', views.test_email, name='test_email'),
    # Add API endpoint for students list
    path('api/students/', views.api_students_list, name='api_students_list'),
]
