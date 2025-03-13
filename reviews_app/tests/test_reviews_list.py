from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from user_auth.models import Seller, Consumer
from reviews_app.models import Review


class ReviewsListTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create_user(
            username='TestUser1', password='password1')
        user_2 = User.objects.create_user(
            username='TestUser2', password='password2')

        cls.seller = Seller.objects.create(user=cls.user_1, type='business')
        cls.consumer = Consumer.objects.create(user=user_2, type='customer')

        cls.token_seller = Token.objects.create(user=cls.user_1)
        cls.token_consumer = Token.objects.create(user=user_2)

        cls.data = {
            "business_user": cls.user_1.id,
            "rating": 4,
            "description": "Alles war toll!"
        }

        cls.url = reverse('reviews')

    def test_get_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'),
                         'Unauthorized. Der Benutzer muss authentifiziert sein.')

    def test_get_authenticated(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_seller.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_unauthenticated(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'),
                         'Unauthorized. Der Benutzer muss authentifiziert sein und ein Kundenprofil besitzen.')

    def test_post_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_seller.key)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertIn('business_user', response.data)
        self.assertIn('reviewer', response.data)
        self.assertIn('rating', response.data)
        self.assertIn('description', response.data)
        self.assertIn('created_at', response.data)
        self.assertIn('updated_at', response.data)
