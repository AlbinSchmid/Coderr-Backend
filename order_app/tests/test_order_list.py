from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from user_auth.models import Seller, Consumer
from offer_app.models import Offer, OfferDetail


class OrderListTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('orders')

        user_1 = User.objects.create_user(
            username='TestUser1', password='password1')
        user_2 = User.objects.create_user(
            username='TestUser2', password='password2')

        cls.seller = Seller.objects.create(user=user_1, type='business')
        cls.consumer = Consumer.objects.create(user=user_2, type='customer')

        cls.offer = Offer.objects.create(
            title='test', description='description', user=user_1
        )
        cls.offerDetail = OfferDetail.objects.create(
            offer=cls.offer,
            title="Basic Design",
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            features=["Logo Design", "Visitenkarte", "Briefpapier"],
            offer_type="basic"
        )

        cls.token_seller = Token.objects.create(user=user_1)
        cls.token_consumer = Token.objects.create(user=user_2)

        cls.data = {
            "offer_detail_id": 1
        }

    def test_get_authenticated(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_seller.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'),
                         'Benutzer ist nicht authentifiziert.')

    def test_post_unauthenticated(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'),
                         'Benutzer ist nicht authentifiziert.')

    def test_post_authenticated_seller(self):
        self.client.credentials()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_seller.key)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'),
                         'Benutzer hat keine Berechtigung, z.B. weil nicht vom typ customer.')

    def test_post_authenticated_consumer(self):
        self.client.credentials()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_consumer.key)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_offer_detail_not_exist(self):
        self.client.credentials()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_consumer.key)
        data = {
            "offer_detail_id": 99999
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('detail'), 'Das angegebene Angebotsdetail wurde nicht gefunden.')

