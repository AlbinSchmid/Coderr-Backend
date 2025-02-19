from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from user_auth.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class ProfileTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='TestUser', password='TestPassword', email="test@gmail.com")
        self.user2 = User.objects.create_user(username='TestUser2', password='TestPassword2', email="test2@gmail.com")
        self.seller = Seller.objects.create(user=self.user, location='Austria', type='business')
        self.consumer = Consumer.objects.create(user=self.user, location='Austria', type='customer')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
    def test_patch_owner_seller(self):
        url = reverse('profile-detail', kwargs={'pk': self.seller.id})
        data = {
            "first_name": "Seller"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('first_name'), 'Seller')
        self.assertEqual(self.seller.location, 'Austria') 

    def test_patch_owner_consumer(self):
        url = reverse('profile-detail', kwargs={'pk': self.consumer.id})
        data = {
            "first_name": "Consumer"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('first_name'), 'Consumer')
        self.assertEqual(self.seller.location, 'Austria') 

    def test_patch_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('profile-detail', kwargs={'pk': self.consumer.id})
        data = {
            "first_name": "Consumer"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Sie sind nicht Berechtig.')

    def test_patch_exist_email(self):
        url = reverse('profile-detail', kwargs={'pk': self.consumer.id})
        data = {
            "email": "test2@gmail.com"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['detail'], 'Diese Email existiert bereits.')

    def test_patch_incorrect_email(self):
        url = reverse('profile-detail', kwargs={'pk': self.consumer.id})
        data = {
            "email": "test2@gmail.c"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Bitte geben Sie eine gültige Email an.')

    def test_get_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('profile-detail', kwargs={'pk': self.consumer.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Sie sind nicht Berechtig.')

    def test_get_not_exist_profile(self):
        url = reverse('profile-detail', kwargs={'pk': 9999999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'User wurde nicht gefunden.')
        