from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('signup/', views.signup, name='signup'),
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('password-reset/', views.password_reset_request, name='password_reset'),
    # path('password-reset-confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    
    # Email Verification URLs
    path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    
]
