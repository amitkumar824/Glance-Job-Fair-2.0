from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Include accounts URLs
    path('accounts/', include('accounts.urls')),
    
    # Dashboard URLs
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    path('dashboard/companies/', views.companies, name='companies'),
    path('dashboard/applications/', views.applications, name='applications'),
    path('dashboard/notifications/', views.notifications, name='notifications'),
    path('dashboard/settings/', views.settings_view, name='settings'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
