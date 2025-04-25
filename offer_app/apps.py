from django.apps import AppConfig


class OfferAppConfig(AppConfig):
    """
    Configuration for the Offer application.
    This class is used to set the default auto field and the name of the application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'offer_app'
