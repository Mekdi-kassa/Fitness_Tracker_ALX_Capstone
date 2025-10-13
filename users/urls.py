from django.urls import path
from . import views

urlpatterns = [
    # Availability check
    path('check-availability/', views.check_availability, name='check-availability'),
    
    # Authentication endpoints
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('google-login/', views.google_login, name='google-login'),
    path('logout/', views.logout_user, name='logout'),
    
    # Profile endpoints
    path('profile/', views.get_user_profile, name='get-profile'),
]