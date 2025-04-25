from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from user_auth.models import Seller, Consumer
from django.urls import reverse
from offer_app.models import Offer, OfferDetail


class OfferDetailTests(APITestCase):
    """
    Test case for the OfferDetailView API endpoint.
    This test case includes tests for creating, updating, and deleting offer details.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the OfferDetailTests class.
        This method is called once for the entire test class.
        """
        user_1 = User.objects.create_user(
            username='TestUser1', password='password1')
        user_2 = User.objects.create_user(
            username='TestUser2', password='password2')

        offer = Offer.objects.create(
            title='test', description='description', user=user_1
        )
        cls.seller = Seller.objects.create(user=user_1, type='business')
        cls.consumer = Consumer.objects.create(user=user_2, type='customer')

        cls.token_user_1 = Token.objects.create(user=user_1)
        cls.token_user_2 = Token.objects.create(user=user_2)

        cls.url = reverse('offer-details', kwargs={'pk': offer.id})
        cls.not_exist_url = reverse('offer-details', kwargs={'pk': 99999})

        cls.data = {
            'title': 'patch'
        }

    def setUp(self):
        """
        Set up the test client and authentication token for each test.
        """
        self.client.credentials()

    def test_get_unauthorized(self):
        """
        Test the GET request for the OfferDetailView API endpoint without authentication.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'),
                         'Benutzer ist nicht authentifiziert.')

    def test_get_authorized(self):
        """
        Test the GET request for the OfferDetailView API endpoint with authentication.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_user_1.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_not_exist(self):
        """
        Test the GET request for a non-existent offer detail.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_user_1.key)
        response = self.client.get(self.not_exist_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get(
            'detail'), 'Das Angebot mit der angegebenen ID wurde nicht gefunden.')

    def test_patch_not_exist(self):
        """
        Test the PATCH request for a non-existent offer detail.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_user_1.key)
        response = self.client.patch(self.not_exist_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get(
            'detail'), 'Das Angebot mit der angegebenen ID wurde nicht gefunden.')

    def test_patch_unauthorized(self):
        """
        Test the PATCH request for the OfferDetailView API endpoint without authentication.
        """
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'),
                         'Benutzer ist nicht authentifiziert.')

    def test_patch_authorized_not_owner(self):
        """
        Test the PATCH request for the OfferDetailView API endpoint with authentication but not as the owner.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_user_2.key)
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get(
            'detail'), 'Authentifizierter Benutzer ist nicht der Eigentümer des Angebots.')

    def test_patch_authorized_owner(self):
        """
        Test the PATCH request for the OfferDetailView API endpoint with authentication as the owner.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_user_1.key)
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), 'patch')

    def test_delete_not_exist(self):
        """
        Test the DELETE request for a non-existent offer detail.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_user_1.key)
        response = self.client.delete(self.not_exist_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get(
            'detail'), 'Das Angebot mit der angegebenen ID wurde nicht gefunden.')

    def test_delete_unauthorized(self):
        """
        Test the DELETE request for the OfferDetailView API endpoint without authentication.
        """
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'),
                         'Benutzer ist nicht authentifiziert.')

    def test_delete_authorized_not_owner(self):
        """
        Test the DELETE request for the OfferDetailView API endpoint with authentication but not as the owner.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_user_2.key)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get(
            'detail'), 'Authentifizierter Benutzer ist nicht der Eigentümer des Angebots.')

    def test_delete_authorized_owner(self):
        """
        Test the DELETE request for the OfferDetailView API endpoint with authentication as the owner.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_user_1.key)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OfferDetailDetailsTest(APITestCase):
    """
    Test case for the OfferDetailView API endpoint.
    This test case includes tests for retrieving offer details.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the OfferDetailDetailsTest class.
        This method is called once for the entire test class.
        """
        user_1 = User.objects.create_user(
            username='TestUser1', password='password1')
        user_2 = User.objects.create_user(
            username='TestUser2', password='password2')

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

        cls.seller = Seller.objects.create(user=user_1, type='business')
        cls.consumer = Consumer.objects.create(user=user_2, type='customer')

        cls.token_user_1 = Token.objects.create(user=user_1)
        cls.token_user_2 = Token.objects.create(user=user_2)

        cls.url = reverse('offerdetail-detail', kwargs={'pk': cls.offerDetail.id})
        cls.not_exist_url = reverse('offerdetail-detail', kwargs={'pk': 99999})

    def setUp(self):
        """
        Set up the test client and authentication token for each test.
        """
        self.client.credentials()

    def test_get_unauthorized(self):
        """
        Test the GET request for the OfferDetailView API endpoint without authentication.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'),
                         'Benutzer ist nicht authentifiziert.')
        
    def test_get_authorized(self):
        """
        Test the GET request for the OfferDetailView API endpoint with authentication.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_user_1.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_not_exist(self):
        """
        Test the GET request for a non-existent offer detail.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_user_1.key)
        response = self.client.get(self.not_exist_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get(
            'detail'), 'Das Angebot mit der angegebenen ID wurde nicht gefunden.')
