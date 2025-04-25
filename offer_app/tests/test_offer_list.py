from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from user_auth.models import Seller, Consumer
from django.urls import reverse


class OfferListTests(APITestCase):
    """
    Test case for the OfferListView API endpoint.
    This test case includes tests for creating and listing offers.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the OfferListTests class.
        This method is called once for the entire test class.
        """
        cls.url = reverse('offers')

        user_1 = User.objects.create_user(
            username='TestUser1', password='password1')
        user_2 = User.objects.create_user(
            username='TestUser2', password='password2')
        
        cls.seller = Seller.objects.create(user=user_1, type='business')
        cls.consumer = Consumer.objects.create(user=user_2, type='customer')

        cls.token_seller = Token.objects.create(user=user_1)
        cls.token_consumer = Token.objects.create(user=user_2)

        cls.data = {
            "title": "Grafikdesign-Paket",
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": [
                        "Logo Design",
                        "Visitenkarte"
                    ],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier"
                    ],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier",
                        "Flyer"
                    ],
                    "offer_type": "premium"
                }
            ]
        }

    def setUp(self):
        """
        Set up the test client and authentication token for each test.
        """
        self.client.credentials()
        
    def test_get_unauthorized(self):
        """
        Test the GET request for the OfferListView API endpoint without authentication.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_authorized_seller(self):
        """
        Test the GET request for the OfferListView API endpoint with authentication.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_seller.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_authorized_consumer(self):
        """
        Test the GET request for the OfferListView API endpoint with authentication.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_consumer.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_unauthorized(self):
        """
        Test the POST request for the OfferListView API endpoint without authentication.
        """
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_authorized_seller(self):
        """
        Test the POST request for the OfferListView API endpoint with authentication.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_seller.key)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('title'), 'Grafikdesign-Paket')

    def test_post_authorized_consumer(self):
        """
        Test the POST request for the OfferListView API endpoint with authentication.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_consumer.key)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
