from django.db import models
from offer_app.models import OfferDetail
from django.contrib.auth.models import User


class Order(models.Model):
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_users', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, default='in_progress')
    offer_detail = models.ForeignKey(OfferDetail, on_delete=models.CASCADE, related_name='offer_detail')
    customer_user = models.ForeignKey(User, on_delete=models.CASCADE)

