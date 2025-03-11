from django.db import models
from django.contrib.auth.models import User
from user_auth.models import Seller
from .api.exeptions import UserHasAlreadyReview
from django.db import IntegrityError

# Create your models here.
class Review(models.Model):
    business_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_user')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    rating = models.IntegerField()
    description = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        try:
            self.clean()
            super().save(*args, **kwargs)
        except IntegrityError:
            raise UserHasAlreadyReview
