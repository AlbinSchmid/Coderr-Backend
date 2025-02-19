from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.


class BaseUserProfile(models.Model):
    type = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Seller(BaseUserProfile):
    location = models.CharField(max_length=255, default='')
    description = models.TextField(max_length=255, default='')
    working_hours = models.CharField(max_length=255, default='')
    tel = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.user.username
    

class Consumer(BaseUserProfile):
    pass
