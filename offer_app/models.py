from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Offer(models.Model):
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='offers/', blank=True, null=True)
    description = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    min_price = models.IntegerField(default=0)
    min_delivery_time = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')


class OfferDetail(models.Model):
    OFFER_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.IntegerField()
    features = models.JSONField(default=list)
    offer_type = models.CharField(choices=OFFER_CHOICES, max_length=15)






