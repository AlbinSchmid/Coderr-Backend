from rest_framework import serializers
from reviews_app.models import Review
from user_auth.models import User
from .exeptions import BadRequest

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.
    """
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
        """
        Meta class for the ReviewSerializer.
        """
        model = Review
        fields = '__all__'
        read_only_fields = ['reviewer']