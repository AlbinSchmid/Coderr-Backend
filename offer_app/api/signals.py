from django.db.models.signals import post_delete
from django.dispatch import receiver
from offer_app.models import Offer

@receiver(post_delete, sender=Offer)
def delete_offer_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(False)