from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum , Count
# Create your models here.
class FitnessActivity(models.Model):
    ACTIVITY_TYPES = [
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('walking', 'Walking'),
        ('weightlifting', 'Weightlifting'),
        ('yoga', 'Yoga'),
        ('pilates', 'Pilates'),
        ('hiit', 'HIIT'),
        ('dancing', 'Dancing'),
        ('hiking', 'Hiking'),
        ('boxing', 'Boxing'),
        ('rowing', 'Rowing'),
        ('skipping', 'Skipping'),
        ('elliptical', 'Elliptical'),
        ('stair_climbing', 'Stair Climbing'),
    ]
    Intensity = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete = models.CASCADE , related_name = 'activities')
    activity_type = models.CharField(max_length = 20 , choices = ACTIVITY_TYPES)
    duration = models.IntegerField(help_text = "duartion in minutes")
    calories_burned = models.IntegerField()
    distance = models.FloatField()
    date = models.DateTimeField(default = timezone.now)
    notes = models.TextField(blank = True)
    intensity = models.CharField(max_length = 10 , choices = Intensity , default = "medium")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    #  now we have created the activity what will be added to the database you can make it this is all baout models
    class Meta:
        ordering = ['-date']
        # to make sorted order when we call the FitnessActivity.objects.all() => sorted order this also can be 
        verbose_name_plural = "Fitness Activities"
        # making model plural naming in django for models
    def __str__(self):
        return f"{self.user.email} - {self.activity_type} - {self.date.strftime('%Y-%m-%d')}"
    def save(self,*args,**kwargs):
        if not self.calories_burned:
            self.calories_burned = self.estimate_calories()
        super().save(*args , **kwargs)
    def estimate_calories(self):
        calorie_rates = {
            'running': 10,
            'cycling': 8,
            'swimming': 7,
            'walking': 4,
            'weightlifting': 6,
            'yoga': 3,
            'pilates': 3,
            'hiit': 12,
            'dancing': 5,
            'hiking': 6,
            'boxing': 9,
            'rowing': 8,
            'skipping': 11,
            'elliptical': 7,
            'stair_climbing': 9,
        }
        base_rate = calorie_rates.get(self.activity_type, 5)
        
        # Adjust for intensity
        intensity_multiplier = {
            'low': 0.7,
            'medium': 1.0,
            'high': 1.3
        }
        
        return int(base_rate * self.duration * intensity_multiplier.get(self.intensity, 1.0))
class WorkoutGoal(models.Model):
    GOAL_TYPE =[
        ('duration', 'Total Duration'),
        ('calories', 'Calories Burned'),
        ('frequency', 'Workout Frequency'),
        ('distance', 'Total Distance'),
        ('streak', 'Workout Streak'),
        ('specific_activity', 'Specific Activity'),
    ]
    DURATION_TYPES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete = models.CASCADE , related_name = 'workout_goals')
    title = models.CharField(max_length = 200)
    description = models.TextField(blank = True)
    goal_type = models.CharField(max_length = 20 , choices = GOAL_TYPE)
    duration_type = models.CharField(max_length = 20 , choices = DURATION_TYPES)
    target_value = models.FloatField(help_text = "Target value (minutes, calories, count, etc.)")
    current_value = models.FloatField(default = 0)
    unit = models.CharField(max_length=20, help_text="minutes, calories, workouts, km, etc.")
    activity_type = models.CharField(max_length=20, choices=FitnessActivity.ACTIVITY_TYPES, blank=True, null=True)
    start_date = models.DateField(default = timezone.now)
    end_date = models.DateField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-created_at"]
    def __str__(self):
        return f"{self.user.email} - {self.title}"
    
    def progress_percentage(self):
        if self.target_value > 0:
            return min(100 , (self.current_value / self.target_value) * 100)
        return 0
    def days_remaining(self):
        today = timezone.now().date()
        remaining = (self.end_date - today).days
        return max(remaining , 0)
    def is_expired(self):
        return timezone.now().date() > self.end_date
    
    def update_progress(self):
        today = timezone.now().date()
        if self.duration_type == 'daily':
            start_date = today
            end_date = today
        elif self.duration_type == "weekly":
            start_date = today - timedelta(days = today.weekday())
            end_date = start_date + timedelta(days=6)
        elif self.duration_type == 'monthly':
            start_date = today.replace(day = 1)
            end_date = (start_date + timedelta(day = 32)).replace(day = 1) - timedelta(days = 1)
        else:
            start_date = today.replace(month = 1 , day = 1)
            end_date = today.replace(month = 12 , day = 31)
        activities = FitnessActivity.objects.filter(
            user=self.user,
            date__date__range=[start_date, end_date]
        )
        if self.activity_type:
            activities = activities.filter(activity_type=self.activity_type)
        
        if self.goal_type == 'duration':
            self.current_value = activities.aggregate(total = Sum('duartion'))['total'] or 0
        elif self.goal_type == "calories":
            self.current_value = activities.aggregate(total = Sum('calories_burned'))['total'] or 0
        elif self.goal_type == 'frequency':
            self.current_value = activities.count()
        elif self.goal_type == 'distance':
            self.current_value = activities.aggregate(total=Sum('distance'))['total'] or 0
        elif self.goal_type == 'streak':
            self.current_value = self.calculate_streak()
        
        # Update status for the profile
        if self.current_value >= self.target_value:
            self.status = 'completed'
        elif self.is_expired() and self.status == 'active':
            self.status = 'failed'
        
        self.save()
    #  counting streaks for the app 
    def calculate_streak(self):
        today = timezone.now().date()
        streak = 0
        for i in range(365):
            check_date = today - timedelta(day = i)
            if FitnessActivity.objects.filter(user = self.user , date_date = check_date).exists():
                streak += 1
            else:
                break
        return streak
class UserProfile(models.Model):
    # we are going to use one profile for one user
    user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete = models.CASCADE , related_name = 'profile')
    total_calories_burned = models.IntegerField(default = 0)
    total_workout_time = models.IntegerField(default = 0)
    current_streak = models.IntegerField(default = 0)
    longest_streak = models.IntegerField(default = 0)
    level = models.IntegerField(default = 1)
    points = models.IntegerField(default = 0)
    last_activity = models.DateField(null = True , blank = True)

    def __str__(self):
        return f"{self.user.email} -Level {self.level}"
    def update_stats(self):
        activities = FitnessActivity.objects.filter(user=self.user)
        
        self.total_calories_burned = activities.aggregate(total=Sum('calories_burned'))['total'] or 0
        self.total_workout_time = activities.aggregate(total=Sum('duration'))['total'] or 0
        self.total_workouts = activities.count()

        self.current_streak = self.calculate_current_streak()
        self.longest_streak = max(self.longest_streak, self.current_streak)

        self.points = (self.total_calories_burned // 100) + self.total_workouts
        

        self.level = (self.points // 100) + 1
        
        self.save()
    def calculate_current_streak(self):
        """Calculate current consecutive days with workouts"""
        today = timezone.now().date()
        streak = 0
        
        for i in range(365):
            check_date = today - timedelta(days=i)
            if FitnessActivity.objects.filter(user=self.user, date__date=check_date).exists():
                streak += 1
            else:
                break
        
        return streak
class Leaderboard(models.Model):
    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('all_time', 'All Time'),
    ]
    period = models.CharField(max_length= 10 , choices = PERIOD_CHOICES)
    snapshot_date = models.DateTimeField(default = timezone.now)
    created_at = models.DateField(auto_now_add = True)
    class Meta:
        ordering = ['-snapshot' , 'period']
    def __str__(self):
        return f"{self.period} Leadersboard - {self.snapshot_date}"
class LeaderboardEntry(models.Model):
    Leadersboard = models.ForeignKey(Leaderboardeaderboard , on_delete=models.CASCADE , related_name = 'entries')
    user = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete = models.CASCADE)
    rank = models.IntegerField()
    points = models.IntegerField()
    calories_burned = models.IntegerField()
    workout_count = models.IntegerField()
    streak = models.IntegerField()
    
    class Meta:
        ordering = ['leaderboard', 'rank']
    
    def __str__(self):
        return f"#{self.rank} - {self.user.email} - {self.points} points"
