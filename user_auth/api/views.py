from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from itertools import chain
from .serializer import *
from .exeptions import *
from .permissions import *


class CustomLogInView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, create = Token.objects.get_or_create(user=user)
    
            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id
            }
            return Response(data, status.HTTP_200_OK)
        else:
            raise LoginNotCorrect
            

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            save_user = serializer.save()
            token, create = Token.objects.get_or_create(user=save_user)
   
            data = {
                'token': token.key,
                'username': save_user.username,
                'email': save_user.email,
                'user_id': save_user.id
            }
            return Response(data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ProfileSingleView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = Consumer.objects.filter(user__id=pk).first() or Seller.objects.filter(user__id=pk).first()
        if not obj:
            raise UserNotFound()

        self.check_object_permissions(self.request, obj) 
        return obj
    
    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = ConsumerSerializer(obj) if isinstance(obj, Consumer) else SellerSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        obj = self.get_object() 
        serializer = ConsumerSerializer(obj, data=request.data, partial=True) if isinstance(obj, Consumer) else SellerSerializer(obj, data=request.data, partial=True)
        user = obj.user

        if serializer.is_valid() and user:
            username = request.data.get('username', user.username)
            email = request.data.get('email', user.email)
            first_name = request.data.get('first_name', user.first_name)
            last_name = request.data.get('last_name', user.last_name)

            try: 
                validate_email = validate_email_address(email, user)
                user.email = validate_email
            except EmailExistAlready:
                raise EmailExistAlready()
            except EmailIncorrect:
                raise EmailIncorrect()

            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            serializer.save()
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
    

class SellerListView(generics.ListAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]


class ConsumerListView(generics.ListAPIView):
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer
    permission_classes = [IsAuthenticated]