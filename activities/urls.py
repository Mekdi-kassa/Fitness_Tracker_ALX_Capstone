from django.urls import path
from . import views

urlpatterns = [
    path('', views.FitnessActivityListCreateView.as_view(), name='activity-list'),
    path('<int:pk>/', views.FitnessActivityDetailView.as_view(), name='activity-detail'),
    path('history/', views.ActivityHistoryView.as_view(), name='activity-history'),
    path('metrics/', views.activity_metrics, name='activity-metrics'),
    path('trends/', views.activity_trends, name='activity-trends'),
    path('recent/', views.recent_activities, name='recent-activities'),
    
    # Workout Goals
    path('goals/', views.WorkoutGoalListCreateView.as_view(), name='goal-list-create'),
    path('goals/<int:pk>/', views.WorkoutGoalDetailView.as_view(), name='goal-detail'),
    
    # Leaderboard
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('leaderboard/my-ranking/', views.my_ranking, name='my-ranking'),
    
    # User Profile
    path('profile/', views.user_profile, name='user-profile'),
]