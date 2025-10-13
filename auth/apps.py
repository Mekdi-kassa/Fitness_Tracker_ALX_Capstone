# auth/apps.py
from django.apps import AppConfig

class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth'
    label = 'custom_auth'  # Keep this - it makes your app unique