from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializer import *
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from .exeptions import *
from itertools import chain


class CustomLogInView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, create = Token.objects.get_or_create(user=user)
            seller = Seller.objects.filter(user__username=user.username).first()
            consumer = Consumer.objects.filter(user__username=user.username).first()
            user_type = ''
            if seller:
                user_type = seller.type
            elif consumer:
                user_type = consumer.type
            
            user_id = ''
            if user_type == 'business':
                user_id = Seller.objects.get(user=user).id
            elif user_type == 'customer':
                user_id = Consumer.objects.get(user=user).id
            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user_id

            }
            return Response(data, status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data, status.HTTP_401_UNAUTHORIZED)
            

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            save_user = serializer.save()
            token, create = Token.objects.get_or_create(user=save_user)
            user_type = serializer.validated_data.get('type')
            user_id = ''
            if user_type == 'business':
                user_id = Seller.objects.get(user=save_user).id
            elif user_type == 'customer':
                user_id = Consumer.objects.get(user=save_user).id
            data = {
                'token': token.key,
                'username': save_user.username,
                'email': save_user.email,
                'user_id': user_id
            }
            return Response(data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ProfileSingleView(generics.RetrieveDestroyAPIView):
    
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        consumer = Consumer.objects.filter(pk=pk).first()
        if consumer:
            serializer = ConsumerSerializer(consumer)
            return Response(serializer.data, status=status.HTTP_200_OK)

        seller = Seller.objects.filter(pk=pk).first()
        if seller:
            serializer = SellerSerializer(seller)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class ProfileListView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        consumer = Consumer.objects.all()
        seller = Seller.objects.all()

        consumer_serializer = ConsumerSerializer(consumer, many=True)
        seller_serializer = SellerSerializer(seller, many=True)

        combined_data = list(chain(consumer_serializer.data, seller_serializer.data))
        return Response(combined_data)