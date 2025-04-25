from django.apps import AppConfig


class UserAuthConfig(AppConfig):
    """
    Configuration for the User Authentication app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_auth'
