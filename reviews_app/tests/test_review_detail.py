from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from user_auth.models import Seller, Consumer
from reviews_app.models import Review


class ReviewDetailTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create_user(
            username='TestUser1', password='password1')
        user_2 = User.objects.create_user(
            username='TestUser2', password='password2')

        cls.seller = Seller.objects.create(user=cls.user_1, type='business')
        cls.consumer = Consumer.objects.create(user=user_2, type='customer')

        cls.review = Review.objects.create(business_user=cls.user_1, reviewer=user_2, description='TEST', rating=5)

        cls.token_seller = Token.objects.create(user=cls.user_1)
        cls.token_consumer = Token.objects.create(user=user_2)

        cls.data = {
            "rating": 4,
            "description": "Alles war toll!"
        }

        cls.url = reverse('review', kwargs={'pk':cls.review.id})

    def test_patch_unauthenticated(self):
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_authenticated_not_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_seller.key)
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'Forbidden. Der Benutzer ist nicht berechtigt, diese Bewertung zu bearbeiten.')

    def test_patch_authenticated_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_consumer.key)
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('description'), 'Alles war toll!')

    def test_patch_authenticated_not_exist(self):
        url = reverse('review', kwargs={'pk': 9999})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_consumer.key)
        response = self.client.patch(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('detail'), 'Nicht gefunden. Es wurde keine Bewertung mit der angegebenen ID gefunden.')

    def test_delete_unauthenticated(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_authenticated_not_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_seller.key)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'Forbidden. Der Benutzer ist nicht berechtigt, diese Bewertung zu löschen.')

    def test_delete_authenticated_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_consumer.key)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_authenticated_not_exist(self):
        url = reverse('review', kwargs={'pk': 9999})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_consumer.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    