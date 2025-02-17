from rest_framework import serializers
from django.contrib.auth.models import User
from user_auth.models import *


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=['customer', 'business'], write_only=True)

    class Meta:
        model = User
        fields = ['username', 'repeated_password', 'password', 'email', 'type']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        email = self.validated_data['email']
        username = self.validated_data['username']
        user_type = self.validated_data['type']

        if pw != repeated_pw:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email already exist.'})
        
        account = User(email=email, username=username)
        account.set_password(pw)
        account.save()

        if user_type == 'business':
            Provider.objects.create(user=account)
        elif user_type == 'customer':
            Consumer.objects.create(user=account)
        else: 
            print('HELLO')
            
        return account