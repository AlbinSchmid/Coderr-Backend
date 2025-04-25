from rest_framework import serializers
from django.contrib.auth.models import User
from user_auth.models import *
from .exeptions import *
from .validators import *
import re


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration. Validates the input data and creates a new user.
    """
    repeated_password = serializers.CharField(write_only=True)
    username = serializers.CharField(validators=[validate_username])
    email = serializers.CharField(validators=[validate_email_address])
    type = serializers.ChoiceField(
        choices=['customer', 'business'], write_only=True)

    class Meta:
        """
        Meta class for the RegistrationSerializer.
        """
        model = User
        fields = ['username', 'repeated_password', 'password', 'email', 'type']
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    def validate(self, data):
        """
        Validate the input data. Check if the password and repeated password match
        and if the email and username are valid.
        """
        validate_password(data['password'], data['repeated_password'])
        return data

    def save(self):
        """
        Create a new user account. Set the password and save the user to the database.
        """
        pw = self.validated_data['password']
        email = self.validated_data['email']
        username = self.validated_data['username']
        user_type = self.validated_data['type']
        first_name = ''
        last_name = ''

        if re.search(r'[._-]', username): 
            parts = re.split(r'[._-]', username)
            first_name = parts[0]
            last_name = parts[1]

        account = User(email=email, username=username, first_name=first_name, last_name=last_name)
        account.set_password(pw)
        account.save()

        if user_type == 'business':
            Seller.objects.create(user=account, type=user_type)
        elif user_type == 'customer':
            Consumer.objects.create(user=account, type=user_type)

        return account


class ConsumerSerializer(serializers.ModelSerializer):
    """
    Serializer for consumer profile. Serializes the consumer data and includes user information.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        """
        Meta class for the ConsumerSerializer.
        """
        model = Consumer
        exclude = ['id']

        
class SellerSerializer(serializers.ModelSerializer):
    """
    Serializer for seller profile. Serializes the seller data and includes user information.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        """
        Meta class for the SellerSerializer.
        """
        model = Seller
        exclude = ['id']
