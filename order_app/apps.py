from django.apps import AppConfig


class OrderAppConfig(AppConfig):
    """
    Configuration for the Order application.
    This class is used to set the default auto field and the name of the application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'order_app'
