from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from user_auth.models import *

class RegistrationTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.registration_url = reverse('registration')

    def test_patch_correct_form_seller(self):
        """Test registration with correct form for seller."""
        data = {
            'username': 'seller',
            'email': 'testuser@example.com',
            'password': 'securepassword123',
            'repeated_password': 'securepassword123',
            'type': 'business'
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Seller.objects.count(), 1)
        self.assertEqual(Consumer.objects.count(), 0)
        self.assertIn('token', response.data),
        self.assertEqual(response.data['username'], 'seller')
        self.assertEqual(response.data['email'], 'testuser@example.com')

    def test_patch_correct_form_consumer(self):
        """Test registration with correct form for consumer."""
        data = {
            'username': 'consumer',
            'email': 'testuser@example.com',
            'password': 'securepassword123',
            'repeated_password': 'securepassword123',
            'type': 'customer'
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Seller.objects.count(), 0)
        self.assertEqual(Consumer.objects.count(), 1)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], 'consumer')
        self.assertEqual(response.data['email'], 'testuser@example.com')

    def test_patch_incorrect_username(self):
        """Test registration with incorrect username."""
        data = {
            'username': 'consumer consumer',
            'email': 'testuser@example.com',
            'password': 'securepassword123',
            'repeated_password': 'securepassword123',
            'type': 'customer'
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Benutzername darf kein Leerzeichen enthalten.')

    def test_patch_already_exist_username(self):
        """Test registration with already existing username."""
        User.objects.create_user(username='consumer', password='password')
        data = {
            'username': 'consumer',
            'email': 'testuser@example.com',
            'password': 'securepassword123',
            'repeated_password': 'securepassword123',
            'type': 'customer'
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Benutzername existiert bereits.')

    def test_patch_incorrect_email(self):
        """Test registration with incorrect email."""
        data = {
            'username': 'consumer',
            'email': 'testuser@example.c',
            'password': 'securepassword123',
            'repeated_password': 'securepassword123',
            'type': 'customer'
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Bitte geben Sie eine gültige Email an.')

    def test_patch_already_exist_email(self):
        """Test registration with already existing email."""
        User.objects.create_user(username='no-username', password='password', email='testuser@example.com')
        data = {
            'username': 'consumer',
            'email': 'testuser@example.com',
            'password': 'securepassword123',
            'repeated_password': 'securepassword123',
            'type': 'customer'
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['detail'], 'Diese Email existiert bereits.')

    def test_patch_password_dont_match(self):
        """Test registration with passwords that don't match."""
        data = {
            'username': 'consumer',
            'email': 'testuser@example.com',
            'password': 'securepassword123',
            'repeated_password': 'securepassword12',
            'type': 'customer'
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Passwörter müssen übereinstimmen.')