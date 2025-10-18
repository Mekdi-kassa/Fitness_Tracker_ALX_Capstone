from rest_framework import serializers
from .models import FitnessActivity,WorkoutGoal,UserProfile,Leaderboard,LeaderboardEntry

class FitnessActivitySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only = True)
    class Meta:
        model = FitnessActivity
        fields = [
            'id', 'user', 'activity_type', 'duration', 'distance', 
            'calories_burned', 'date', 'notes', 'intensity',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('user', 'created_at', 'updated_at')
        def validated_duration(self , value):
            if value <= 0:
                raise serializers.ValidationError("Duration must be greater than 0 minutes.")

            if value > 1440:
                raise serializers.ValidationError("Duration cannot exceed 1440 minutes (24 hours).")

            return value
        def validate_distance(self, value):
            if value is not None and value < 0:
                raise serializers.ValidationError("Distance cannot be negative.")
            return value
        
        def validate_calories_burned(self, value):
            if value <= 0:
                raise serializers.ValidationError("Calories burned must be greater than 0.")
            return value
class ActivityMetricsSerializer(serializers.Serializer):
    total_duration = serializers.IntegerField()
    total_distance = serializers.FloatField()
    total_calories = serializers.IntegerField()
    activity_count = serializers.IntegerField()
    average_duration = serializers.FloatField()
    average_calories = serializers.FloatField()

class ActivityTrendSerializer(serializers.Serializer):
    period = serializers.CharField()
    total_duration = serializers.IntegerField()
    total_calories = serializers.IntegerField()
    activity_count = serializers.IntegerField()
    date = serializers.CharField()

class WorkoutGoalSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()
    is_expierd = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(read_only = True)
    class Meta:
        models = WorkoutGoal
        fields = [
            'id', 'user', 'title', 'description', 'goal_type', 'duration_type',
            'target_value', 'current_value', 'unit', 'activity_type',
            'start_date', 'end_date', 'status', 'progress_percentage',
            'days_remaining', 'is_expired', 'created_at'
        ]
        read_only_fields = ('user', 'current_value', 'status')
        def get_progress_percentage(self,obj):
            return obj.progress_percentage()
        
        def get_days_remaining(self, obj):
            return obj.days_remaining()
        
        def get_is_expired(self, obj):
            return obj.is_expired()
    
        def create(self, validated_data):
            validated_data['user'] = self.context['request'].user
            return super().create(validated_data)
class UserProfileSeriallizer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only = True)
    username = serializers.CharField(source = 'user.username' ,read_only = True)
    email = serializers.CharField(source = 'user.email' ,read_only = True)

    class Meta:
        model = UserProfile
        fields = [
            'user', 'username', 'email', 'total_calories_burned', 
            'total_workout_time', 'total_workouts', 'current_streak',
            'longest_streak', 'level', 'points', 'last_activity_date'
        ]

class LeaderboardEntrySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source = 'user.username' ,read_only = True)
    email = serializers.CharField(source = 'user.email' ,read_only = True)
    class Meta:
        model = LeaderboardEntry
        fields = [
           'rank', 'username', 'email', 'points', 'calories_burned', 'workout_count', 'streak' 
        ]
class LeaderboardSerializer(serializers.ModelSerializer):
    entries = LeaderboardEntrySerializer(many = True , read_only = True)
    class Meta:
        model = Leaderboard
        fields = [
            'id', 'period', 'snapshot_date', 'entries', 'created_at'
        ]