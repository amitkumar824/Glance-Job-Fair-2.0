from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    
    path('logout/', views.logout_view, name='logout'),
    # path('password-reset/', views.password_reset_request, name='password_reset'),
    # path('password-reset-confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    
    # Email Verification URLs
    path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    
]
=======
    path('profile/', views.profile, name='profile'),
    path('profile/upload-resume/', views.upload_resume, name='upload_resume'),
    path('profile/add-certificate/', views.add_certificate, name='add_certificate'),
    path('update-theme/', views.update_theme, name='update_theme'),
] 
>>>>>>> 1687bb20997a2c7c07f6827d1b8042b382a0a73d
