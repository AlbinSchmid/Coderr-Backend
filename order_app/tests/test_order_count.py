from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from user_auth.models import Seller, Consumer
from offer_app.models import Offer, OfferDetail
from order_app.models import Order

class OrderCountTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
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
        cls.order = Order.objects.create(
            offer_detail_id=cls.offerDetail.id, customer_user=user_2)
        
        cls.url_count = reverse('order-count', kwargs={'pk': user_1.id})
        cls.url_completed_count = reverse('complete-order-count', kwargs={'pk': user_1.id})

        cls.token_seller = Token.objects.create(user=user_1)
        cls.token_consumer = Token.objects.create(user=user_2)
        
    def test_get_authenticated(self):
        self.client.credentials()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_consumer.key)
        response = self.client.get(self.url_count)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('order_count'), 1)

    def test_get_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url_count)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'), 'Benutzer ist nicht authentifiziert.')

    def test_get_not_exist_pk(self):
        self.client.credentials()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_consumer.key)
        url = reverse('order-count', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('detail'), 'Kein Geschäftsnutzer mit der angegebenen ID gefunden.')

    def test_get_completed_authenticated(self):
        self.client.credentials()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_consumer.key)
        response = self.client.get(self.url_completed_count)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('completed_order_count'), 0)

    def test_get_completed_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url_completed_count)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'), 'Benutzer ist nicht authentifiziert.')

    def test_get_completed_not_exist_pk(self):
        self.client.credentials()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_consumer.key)
        url = reverse('order-count', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('detail'), 'Kein Geschäftsnutzer mit der angegebenen ID gefunden.')

    