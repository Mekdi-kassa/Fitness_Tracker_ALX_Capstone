from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import Sum, Count, Avg
from .models import (
    FitnessActivity,
    WorkoutGoal,
    Leaderboard,
    LeaderboardEntry,
    UserProfile
)
from .serializers import (
    FitnessActivitySerializer,
    ActivityMetricsSerializer,
    ActivityTrendSerializer,
    WorkoutGoalSerializer,
    LeaderboardSerializer,
    LeaderboardEntrySerializer,
    UserProfileSeriallizer
)

### -------------------- FITNESS ACTIVITY VIEWS --------------------

class FitnessActivityListCreateView(generics.ListCreateAPIView):
    serializer_class = FitnessActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FitnessActivity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FitnessActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FitnessActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FitnessActivity.objects.filter(user=self.request.user)


class ActivityHistoryView(generics.ListAPIView):
    serializer_class = FitnessActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = FitnessActivity.objects.filter(user=self.request.user)

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        activity_type = self.request.query_params.get('activity_type')

        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__date__gte=start_date)
            except ValueError:
                pass

        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__date__lte=end_date)
            except ValueError:
                pass

        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)

        return queryset

### -------------------- WORKOUT GOALS --------------------

class WorkoutGoalListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkoutGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WorkoutGoal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkoutGoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkoutGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WorkoutGoal.objects.filter(user=self.request.user)

### -------------------- METRICS & TRENDS --------------------

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def activity_metrics(request):
    user = request.user
    period = request.query_params.get('period', 'all')

    queryset = FitnessActivity.objects.filter(user=user)
    today = timezone.now().date()

    if period == "week":
        start_date = today - timedelta(days=7)
        queryset = queryset.filter(date__date__gte=start_date)
    elif period == "month":
        start_date = today - timedelta(days=30)
        queryset = queryset.filter(date__date__gte=start_date)
    elif period == "year":
        start_date = today - timedelta(days=365)
        queryset = queryset.filter(date__date__gte=start_date)

    metrics = queryset.aggregate(
        total_duration=Sum('duration'),
        total_distance=Sum('distance'),
        total_calories=Sum('calories_burned'),
        activity_count=Count('id'),
        average_duration=Avg('duration'),
        average_calories=Avg('calories_burned')
    )
    metrics = {k: v or 0 for k, v in metrics.items()}

    serializer = ActivityMetricsSerializer(metrics)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def activity_trends(request):
    user = request.user
    trend_type = request.query_params.get('trend_type', 'weekly')

    today = timezone.now().date()
    trends = []

    if trend_type == 'weekly':
        for i in range(8):
            week_start = today - timedelta(weeks=i + 1)
            week_end = today - timedelta(weeks=i)

            activities = FitnessActivity.objects.filter(
                user=user,
                date__date__gte=week_start,
                date__date__lt=week_end
            )

            metrics = activities.aggregate(
                total_duration=Sum('duration'),
                total_calories=Sum('calories_burned'),
                activity_count=Count('id')
            )

            trends.append({
                'period': 'weekly',
                'total_duration': metrics['total_duration'] or 0,
                'total_calories': metrics['total_calories'] or 0,
                'activity_count': metrics['activity_count'] or 0,
                'date': week_start.strftime('%Y-%m-%d')
            })

    elif trend_type == 'monthly':
        for i in range(6):
            month_start = today.replace(day=1) - timedelta(days=30 * i)
            month_end = month_start + timedelta(days=30)

            activities = FitnessActivity.objects.filter(
                user=user,
                date__date__gte=month_start,
                date__date__lt=month_end
            )

            metrics = activities.aggregate(
                total_duration=Sum('duration'),
                total_calories=Sum('calories_burned'),
                activity_count=Count('id')
            )

            trends.append({
                'period': 'monthly',
                'total_duration': metrics['total_duration'] or 0,
                'total_calories': metrics['total_calories'] or 0,
                'activity_count': metrics['activity_count'] or 0,
                'date': month_start.strftime('%Y-%m')
            })

    trends.reverse()
    serializer = ActivityTrendSerializer(trends, many=True)
    return Response(serializer.data)

### -------------------- RECENT ACTIVITIES --------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recent_activities(request):
    user = request.user
    limit = int(request.query_params.get('limit', 10))
    activities = FitnessActivity.objects.filter(user=user).order_by('-date')[:limit]
    serializer = FitnessActivitySerializer(activities, many=True)

    return Response({
        'recent_activities': serializer.data,
        'total_count': FitnessActivity.objects.filter(user=user).count()
    })

### -------------------- LEADERBOARD --------------------

def update_leaderboard(leaderboard_obj, period):
    leaderboard_obj.entries.all().delete()
    today = timezone.now().date()

    if period == "daily":
        start_date = today
    elif period == "weekly":
        start_date = today - timedelta(days=7)
    elif period == "monthly":
        start_date = today - timedelta(days=30)
    else:
        start_date = None

    profiles = UserProfile.objects.all()
    entries = []

    for profile in profiles:
        if start_date:
            activities = FitnessActivity.objects.filter(
                user=profile.user,
                date__date__gte=start_date
            )
            calories = activities.aggregate(total=Sum('calories_burned'))['total'] or 0
            points = (calories // 100) + activities.count()
            workouts = activities.count()
            streak = profile.calculate_current_streak()
        else:
            points = profile.points
            calories = profile.total_calories_burned
            workouts = profile.total_workouts
            streak = profile.current_streak

        entries.append(LeaderboardEntry(
            leaderboard=leaderboard_obj,
            user=profile.user,
            points=points,
            calories_burned=calories,
            workout_count=workouts,
            streak=streak
        ))

    entries.sort(key=lambda x: x.points, reverse=True)
    for rank, entry in enumerate(entries, start=1):
        entry.rank = rank

    LeaderboardEntry.objects.bulk_create(entries)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leaderboard(request):
    period = request.query_params.get('period', 'weekly')

    leaderboard_obj, created = Leaderboard.objects.get_or_create(
        period=period,
        snapshot_date=timezone.now().date(),
        defaults={'period': period}
    )

    if created or not leaderboard_obj.entries.exists():
        update_leaderboard(leaderboard_obj, period)

    serializer = LeaderboardSerializer(leaderboard_obj)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_ranking(request):
    period = request.query_params.get('period', 'weekly')
    leaderboard_obj = Leaderboard.objects.filter(
        period=period,
        snapshot_date=timezone.now().date()
    ).first()

    if not leaderboard_obj:
        return Response({'error': 'Leaderboard not found'}, status=404)

    entry = leaderboard_obj.entries.filter(user=request.user).first()
    if not entry:
        return Response({'error': 'User not in leaderboard'}, status=404)

    serializer = LeaderboardEntrySerializer(entry)
    return Response(serializer.data)

### -------------------- USER PROFILE --------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if created or request.query_params.get('refresh'):
        profile.update_stats()

    serializer = UserProfileSeriallizer(profile)
    return Response(serializer.data)
