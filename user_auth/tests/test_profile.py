from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from user_auth.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class ProfileTests(APITestCase):
    """
    Test case for the Profile API endpoint.
    This class contains tests for the PATCH and GET methods of the Profile API.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the ProfileTests class.
        This method creates test users, sellers, consumers, and a token for authentication.
        """
        user = User.objects.create_user(username='TestUser', password='TestPassword', email="test@gmail.com")
        cls.user2 = User.objects.create_user(username='TestUser2', password='TestPassword2', email="test2@gmail.com")

        cls.seller = Seller.objects.create(user=user, location='Austria', type='business')
        cls.consumer = Consumer.objects.create(user=user, type='customer')
        
        cls.token = Token.objects.create(user=user)

    def setUp(self):
        """
        Set up the test client and authenticate the user.
        This method is called before each test method is executed.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
    def test_patch_owner_seller(self):
        """Test patching the seller profile with valid data."""
        url = reverse('profile-detail', kwargs={'pk': self.seller.user.id})
        data = {
            "first_name": "Seller"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('first_name'), 'Seller')
        self.assertEqual(self.seller.location, 'Austria') 

    def test_patch_owner_consumer(self):
        """Test patching the consumer profile with valid data."""
        url = reverse('profile-detail', kwargs={'pk': self.consumer.user.id})
        data = {
            "first_name": "Consumer"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('first_name'), 'Consumer')

    def test_patch_unauthorized(self):
        """Test patching the profile without authentication."""
        self.client.force_authenticate(user=None)
        url = reverse('profile-detail', kwargs={'pk': self.consumer.user.id})
        data = {
            "first_name": "Consumer"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Authentifizierter Benutzer ist nicht der Eigentümer Profils.')

    def test_patch_not_owner(self):
        """Test patching the profile as a different user."""
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
        """Test patching a non-existent profile."""
        url = reverse('profile-detail', kwargs={'pk': 9999999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Das Benutzerprofil wurde nicht gefunden.')

    def test_patch_exist_email(self):
        """Test patching the profile with an existing email."""
        url = reverse('profile-detail', kwargs={'pk': self.consumer.user.id})
        data = {
            "email": "test2@gmail.com"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['detail'], 'Diese Email existiert bereits.')

    def test_patch_incorrect_email(self):
        """Test patching the profile with an incorrect email."""
        url = reverse('profile-detail', kwargs={'pk': self.consumer.user.id})
        data = {
            "email": "test2@gmail.c"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Bitte geben Sie eine gültige Email an.')

    def test_get_unauthorized(self):
        """Test getting the profile without authentication."""
        self.client.force_authenticate(user=None)
        url = reverse('profile-detail', kwargs={'pk': self.consumer.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Benutzer ist nicht authentifiziert.')

    def test_get_not_exist_profile(self):
        """Test getting a non-existent profile."""
        url = reverse('profile-detail', kwargs={'pk': 9999999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Das Benutzerprofil wurde nicht gefunden.')

    def test_get_consumer_authorized(self):
        """Test getting the consumer profile with valid data."""
        url = reverse('consumer')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_seller_authorized(self):
        """Test getting the seller profile with valid data."""
        url = reverse('seller')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_consumer_unauthorized(self):
        """Test getting the consumer profile without authentication."""
        self.client.force_authenticate(user=None)
        url = reverse('consumer')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_seller_unauthorized(self):
        """Test getting the seller profile without authentication."""
        self.client.force_authenticate(user=None)
        url = reverse('seller')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)