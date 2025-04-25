from django.apps import AppConfig


class BaseInfoAppConfig(AppConfig):
    """
    Configuration for the Base Info application.
    This class is used to set the default auto field and the name of the application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_info_app'
