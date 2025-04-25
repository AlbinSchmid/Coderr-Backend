from django.db import models
from django.contrib.auth.models import User
from user_auth.models import Seller
from .api.exeptions import UserHasAlreadyReview
from django.db import IntegrityError

# Create your models here.
class Review(models.Model):
    """
    Model representing a review for a business user.
    """
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    rating = models.IntegerField()
    description = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for the Review model.
        """
        unique_together = ('business_user', 'reviewer')

    def clean(self):
        """
        Validate the review instance before saving.
        Check if the reviewer is a business user and if the review already exists.
        """
        if self.pk is None:
            if Review.objects.filter(business_user=self.business_user, reviewer=self.reviewer).exists():
                raise UserHasAlreadyReview
        
    def save(self, *args, **kwargs):
        """
        Save the review instance to the database.
        Call the clean method to validate the instance before saving.
        """
        self.clean() 
        super().save(*args, **kwargs) 
