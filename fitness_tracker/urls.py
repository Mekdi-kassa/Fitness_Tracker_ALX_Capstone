from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        'message': 'Fitness Tracker API is running!',
        'endpoints': {
            'admin': '/admin/',
            'api_auth': '/api/auth/',
            'register': '/api/auth/register/',
            'login': '/api/auth/login/',
            'google_login': '/api/auth/google-login/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('auth.urls')),
    path('', home, name='home'),
]