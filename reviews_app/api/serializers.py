from rest_framework import serializers
from reviews_app.models import Review
from user_auth.models import User

class ReviewSerializer(serializers.ModelSerializer):
    business_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['reviewer']