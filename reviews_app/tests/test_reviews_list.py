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
        cls.user_seller_1 = User.objects.create_user(
            username='Seller1', password='Seller1')
        cls.user_seller_2 = User.objects.create_user(
            username='Seller2', password='Seller2')
        cls.user_consumer_1 = User.objects.create_user(
            username='Consumer1', password='Consumer1')
        cls.user_consumer_2 = User.objects.create_user(
            username='Consumer2', password='Consumer2')

        Seller.objects.create(user=cls.user_seller_1, type='business')
        Seller.objects.create(user=cls.user_seller_2, type='business')
        Consumer.objects.create(user=cls.user_consumer_1, type='customer')
        Consumer.objects.create(user=cls.user_consumer_2, type='customer')

        Review.objects.create(business_user=cls.user_seller_1, rating=1, description='TestForFilter', reviewer=cls.user_consumer_2)
        Review.objects.create(business_user=cls.user_seller_2, rating=1, description='TestForFilter', reviewer=cls.user_consumer_2)

        cls.token_seller = Token.objects.create(user=cls.user_seller_1)
        cls.token_consumer = Token.objects.create(user=cls.user_consumer_1)

        cls.data = {
            "business_user": cls.user_seller_1.id,
            "rating": 4,
            "description": "TestForPost"
        }

        cls.url = reverse('reviews')

    def setUp(self):
        self.client.credentials()

    def test_get_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'),
                         'Unauthorized. Der Benutzer muss authentifiziert sein.')

    def test_get_authenticated_seller(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_seller.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_authenticated_consumer(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_consumer.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_correct_filter_return_single_result(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_seller.key)
        response = self.client.get(f'/api/reviews/?business_user_id={self.user_seller_1.id}&reviewer_id={self.user_consumer_2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertTrue(all(review["business_user"] == self.user_seller_1.id for review in response.json()))
        self.assertTrue(all(review["reviewer"] == self.user_consumer_2.id for review in response.json()))

    def test_incorrect_filters_return_none_result(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_seller.key)
        response = self.client.get(f'/api/reviews/?business_user_id=777&reviewer_id=888')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    def test_str_filters_return_error(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_seller.key)
        response = self.client.get(f'/api/reviews/?business_user_id={''}&reviewer_id={'asdf'}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Ungültige Anfrageparameter.')

    def test_post_unauthenticated(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'),
                         'Unauthorized. Der Benutzer muss authentifiziert sein und ein Kundenprofil besitzen.')

    def test_post_authenticated_seller(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_seller.key)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'Forbidden. Der Bentutzer ist kein typ vom Consumer.')

    def test_post_authenticated_consumer(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_consumer.key)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["business_user"], self.user_seller_1.id)
        self.assertEqual(response.data["reviewer"], self.user_consumer_1.id)

    def test_post_authenticated_consumer_double_review(self):
        Review.objects.create(business_user=self.user_seller_1, rating=1, description='TestForFilter', reviewer=self.user_consumer_1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_consumer.key)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'Forbidden. Ein Benutzer kann nur eine Bewertung pro Geschäftsprofil abgeben.')

    def test_post_authenticated_seller_double_review(self):
        Review.objects.create(business_user=self.user_seller_1, rating=1, description='TestForFilter', reviewer=self.user_consumer_1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_seller.key)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'Forbidden. Der Bentutzer ist kein typ vom Consumer.')

    
