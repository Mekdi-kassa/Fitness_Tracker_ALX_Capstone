from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import FitnessActivity, UserProfile, WorkoutGoal

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=FitnessActivity)
def update_user_stats(sender, instance, created, **kwargs):
    if created:
        # Update user profile
        if hasattr(instance.user, 'profile'):
            instance.user.profile.update_stats()
        
        # Update all active goals for this user
        active_goals = WorkoutGoal.objects.filter(user=instance.user, status='active')
        for goal in active_goals:
            goal.update_progress()