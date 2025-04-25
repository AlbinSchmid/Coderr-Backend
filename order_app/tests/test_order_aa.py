from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from user_auth.models import Seller, Consumer
from offer_app.models import Offer, OfferDetail


class OrderListTests(APITestCase):
    """
    Test case for the OrderListView API endpoint.
    This test case includes tests for creating and listing orders.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the OrderListTests class.
        This method is called once for the entire test class.
        """
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
        """
        Test the GET request for the OrderListView API endpoint with an authenticated user.
        """
        url = reverse('orders')
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_seller.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_unauthenticated(self):
        """
        Test the POST request for the OrderListView API endpoint with an unauthenticated user.
        """
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

