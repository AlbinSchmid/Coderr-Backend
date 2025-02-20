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
        self.consumer = Consumer.objects.create(user=self.user, type='customer')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
    def test_patch_owner_seller(self):
        url = reverse('profile-detail', kwargs={'pk': self.seller.user.id})
        data = {
            "first_name": "Seller"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('first_name'), 'Seller')
        self.assertEqual(self.seller.location, 'Austria') 

    def test_patch_owner_consumer(self):
        url = reverse('profile-detail', kwargs={'pk': self.consumer.user.id})
        data = {
            "first_name": "Consumer"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('first_name'), 'Consumer')

    def test_patch_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('profile-detail', kwargs={'pk': self.consumer.user.id})
        data = {
            "first_name": "Consumer"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Authentifizierter Benutzer ist nicht der Eigentümer Profils.')

    def test_patch_not_owner(self):
        self.client.force_authenticate(user=None)
        self.token = Token.objects.create(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('profile-detail', kwargs={'pk': self.consumer.user.id})
        data = {
            "first_name": "Consumer"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Authentifizierter Benutzer ist nicht der Eigentümer Profils.')

    def test_patch_not_exist_profile(self):
        url = reverse('profile-detail', kwargs={'pk': 9999999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Das Benutzerprofil wurde nicht gefunden.')

    def test_patch_exist_email(self):
        url = reverse('profile-detail', kwargs={'pk': self.consumer.user.id})
        data = {
            "email": "test2@gmail.com"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['detail'], 'Diese Email existiert bereits.')

    def test_patch_incorrect_email(self):
        url = reverse('profile-detail', kwargs={'pk': self.consumer.user.id})
        data = {
            "email": "test2@gmail.c"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Bitte geben Sie eine gültige Email an.')

    def test_get_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('profile-detail', kwargs={'pk': self.consumer.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Benutzer ist nicht authentifiziert.')

    def test_get_not_exist_profile(self):
        url = reverse('profile-detail', kwargs={'pk': 9999999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Das Benutzerprofil wurde nicht gefunden.')

    def test_get_consumer_authorized(self):
        url = reverse('consumer')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_consumer_authorized(self):
        url = reverse('seller')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_consumer_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('consumer')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_seller_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('seller')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)