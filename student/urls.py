from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard'),
    path('profile/', views.profile, name='myProfile'),
    path('companies/', views.companies, name='all_companies'),
    path('applications/', views.applications, name='my_applications'),
    path('notifications/', views.notifications, name='notifications'),
    path('settings/', views.settings_view, name='settings'),

]
