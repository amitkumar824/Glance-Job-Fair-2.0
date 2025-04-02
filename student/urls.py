from django.urls import path
from . import views

<<<<<<< HEAD
app_name = 'student'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
=======
urlpatterns = [
    path('', views.dashboard_home, name='dashboard'),
    path('profile/', views.profile, name='myProfile'),
    path('companies/', views.companies, name='all_companies'),
    path('applications/', views.applications, name='my_applications'),
    path('notifications/', views.notifications, name='notifications'),
    path('settings/', views.settings_view, name='settings'),

>>>>>>> 1687bb20997a2c7c07f6827d1b8042b382a0a73d
]
