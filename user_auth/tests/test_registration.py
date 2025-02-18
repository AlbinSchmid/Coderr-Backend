from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from user_auth.models import *


class RegistrationTest(APITestCase):

    def test_registration_seller(self):
        url = reverse('registration')
        data = {
            'username': 'seller',
            'email': 'testuser@example.com',
            'password': 'securepassword123',
            'repeated_password': 'securepassword123',
            'type': 'business'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Seller.objects.count(), 1)
        self.assertEqual(Consumer.objects.count(), 0)
        self.assertIn('token', response.data),
        self.assertEqual(response.data['username'], 'seller')
        self.assertEqual(response.data['email'], 'testuser@example.com')

    def test_registration_consumer(self):
        url = reverse('registration')
        data = {
            'username': 'consumer',
            'email': 'testuser@example.com',
            'password': 'securepassword123',
            'repeated_password': 'securepassword123',
            'type': 'customer'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Seller.objects.count(), 0)
        self.assertEqual(Consumer.objects.count(), 1)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], 'consumer')
        self.assertEqual(response.data['email'], 'testuser@example.com')
    
