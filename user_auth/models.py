from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class BaseUserProfile(models.Model):
    """
    Abstract base class for user profiles. This class contains common fields
    and methods that can be inherited by other user profile models.
    """
    type = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta class for the BaseUserProfile model.
        """
        abstract = True


class Seller(BaseUserProfile):
    """
    Seller profile model. Inherits from BaseUserProfile and adds additional fields
    specific to sellers.
    """
    location = models.CharField(max_length=255, default='')
    description = models.TextField(max_length=255, default='')
    working_hours = models.CharField(max_length=255, default='')
    tel = models.CharField(max_length=255, default='')

    def __str__(self):
        """
        String representation of the Seller model.
        Returns the username of the associated user.
        """
        return self.user.username
    

class Consumer(BaseUserProfile):
    """
    Consumer profile model. Inherits from BaseUserProfile and adds additional fields
    specific to consumers.
    """
    pass
