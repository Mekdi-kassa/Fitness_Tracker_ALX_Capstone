from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # The importable Python package name for this app (it's a top-level package in this project).
    name = 'auth'
    # Use a different label to avoid colliding with Django's built-in `auth` app label.
    label = 'custom_auth'  # database/app label (must be unique)
    verbose_name = 'Custom Authentication'