from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
<<<<<<< HEAD

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('student.urls')),
    path('administration/', include('administrator.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

=======
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
    path("dashboard/", include("student.urls")),

]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> 1687bb20997a2c7c07f6827d1b8042b382a0a73d
