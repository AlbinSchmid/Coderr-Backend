from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BaseUserProfile(models.Model):
    type = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # profile_file = models.ImageField(null=True, blank=True)
    location = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True, max_length=255)
    working_hours = models.CharField(null=True, blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Seller(BaseUserProfile):
    pass
    def __str__(self):
        return self.user.username
    

class Consumer(BaseUserProfile):
    pass
