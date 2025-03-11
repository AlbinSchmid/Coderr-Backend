from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from user_auth.models import Seller, Consumer
from offer_app.models import Offer, OfferDetail
from order_app.models import Order


class OrderDetailTests(APITestCase):

    @classmethod
    def setUpTestData(cls):

        user_1 = User.objects.create_user(
            username='TestUser1', password='password1')
        user_2 = User.objects.create_user(
            username='TestUser2', password='password2')
        user_3 = User.objects.create_user(
            username='TestUser3', password='password3')
        user_3.is_staff = True
        user_3.save()

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
            offer_detail_id=1, customer_user=user_2)

        cls.token_seller = Token.objects.create(user=user_1)
        cls.token_consumer = Token.objects.create(user=user_2)
        cls.token_staff = Token.objects.create(user=user_3)
        

        cls.data = {
            "status": "completed"
        }

        cls.url = reverse('order', kwargs={'pk': cls.order.id})

    def test_patch_unauthenticated(self):
        respone = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(respone.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(respone.data.get('detail'),
                         'Benutzer ist nicht authentifiziert.')
        
    def test_patch_authenticated_seller(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_seller.key)
        respone = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(respone.status_code, status.HTTP_200_OK)
        self.assertEqual(respone.data.get('status'), 'completed')

    def test_patch_authenticated_consumer(self):
        self.client.credentials()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_consumer.key)
        respone = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(respone.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(respone.data.get('detail'),
                         'Benutzer hat keine Berechtigung, diese Bestellung zu aktualisieren.')
        
    def test_patch_not_exist_order(self):
        self.client.credentials()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_seller.key)
        url = reverse('order', kwargs={'pk': 9999})
        respone = self.client.patch(url, self.data, format='json')
        self.assertEqual(respone.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(respone.data.get('detail'),
                         'Die angegebene Bestellung wurde nicht gefunden.')
        
    def test_delete_unauthenticated(self):
        respone = self.client.delete(self.url)
        self.assertEqual(respone.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(respone.data.get('detail'),
                         'Benutzer ist nicht authentifiziert.')
        self.assertEqual(Order.objects.count(), 1)
        
    def test_delete_authenticated_no_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_seller.key)
        respone = self.client.delete(self.url)
        self.assertEqual(respone.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(respone.data.get('detail'), 'Benutzer hat keine Berechtigung, die Bestellung zu löschen.')
        self.assertEqual(Order.objects.count(), 1)

    def test_delete_authenticated_staff(self):
        self.client.credentials()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_staff.key)
        initial_count = Order.objects.count()
        respone = self.client.delete(self.url)
        self.assertEqual(respone.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), initial_count - 1)

    def test_delete_not_exist_order(self):
        self.client.credentials()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_staff.key)
        url = reverse('order', kwargs={'pk': 9999})
        respone = self.client.delete(url)
        self.assertEqual(respone.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(respone.data.get('detail'),
                         'Die angegebene Bestellung wurde nicht gefunden.')
        
    

