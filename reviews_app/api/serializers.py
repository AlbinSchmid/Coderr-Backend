from rest_framework import serializers
from reviews_app.models import Review
from user_auth.models import User
from .exeptions import BadRequest

class ReviewSerializer(serializers.ModelSerializer):
    business_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    rating = serializers.IntegerField(
        error_messages={
            'invalid': 'Rating muss eine Zahl sein.',
            'required': 'Rating ist ein Pflichtfeld.'
        }
    )
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['reviewer']