from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from user_auth.models import *
from .exeptions import *


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    email = serializers.CharField(validators=[])
    type = serializers.ChoiceField(
        choices=['customer', 'business'], write_only=True)

    class Meta:
        model = User
        fields = ['username', 'repeated_password', 'password', 'email', 'type']
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
            'username': {
                'validators': []
            },
            'email': {
                'validators': []
            }
        }

    def validate_username(self, value):
        if " " in value:
            raise UsernameContainsSpace()
        if User.objects.filter(username=value).exists():
            raise UsernameExistAlready()
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise EmailExistAlready()
        try:
            validate_email(value) 
        except ValidationError:
            raise EmailIncorrect()
        return value

    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        email = self.validated_data['email']
        username = self.validated_data['username']
        user_type = self.validated_data['type']
        print(username)
        if pw != repeated_pw:
            raise serializers.ValidationError(
                {'password': 'Passwords must match.'})

        if User.objects.filter(email=email).exists():

            raise serializers.ValidationError(
                {'email': 'Email already exist.'})

        account = User(email=email, username=username)
        account.set_password(pw)
        account.save()

        if user_type == 'business':
            Seller.objects.create(user=account, type=user_type)
        elif user_type == 'customer':
            Consumer.objects.create(user=account, type=user_type)
        else:
            print('HELLO')

        return account


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Consumer
        fields = '__all__'
