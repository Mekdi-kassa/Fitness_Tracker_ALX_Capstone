from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

def home(request):
    return JsonResponse({
        'message': '🏋️ Fitness Tracker API is running!',
        'endpoints': {
            'admin': '/admin/',
            'api_auth': '/api/auth/',
            'register': '/api/auth/register/',
            'login': '/api/auth/login/',
            'google_login': '/api/auth/google-login/',
            'activities': {
                'base': '/api/activities/',
                'docs': {
                    'list_create': 'GET/POST /api/activities/activities/',
                    'detail': 'GET/PUT/DELETE /api/activities/activities/{id}/',
                    'history': 'GET /api/activities/history/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&activity_type=running',
                    'metrics': 'GET /api/activities/metrics/?period=week|month|year|all',
                    'trends': 'GET /api/activities/trends/?trend_type=weekly|monthly',
                    'recent': 'GET /api/activities/recent/?limit=10',
                }
            },
            'workout_goals': {
                'list_create': 'GET/POST /api/activities/goals/',
                'detail': 'GET/PUT/DELETE /api/activities/goals/{id}/',
            },
            'leaderboard': {
                'get_leaderboard': 'GET /api/activities/leaderboard/?period=daily|weekly|monthly',
                'my_ranking': 'GET /api/activities/leaderboard/my-ranking/?period=daily|weekly|monthly',
            },
            'user_profile': {
                'get_profile': 'GET /api/activities/profile/',
                'refresh_profile': 'GET /api/activities/profile/?refresh=true',
            }
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/auth/', include('users.urls')),       # Handles register, login, google login
    path('api/activities/', include('activities.urls')),  # Your main app
    path('', home, name='home'),
]
