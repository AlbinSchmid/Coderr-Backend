from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializer import *
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from .exeptions import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class CustomLogInView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, create = Token.objects.get_or_create(user=user)
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
            pass
            # save_user = serializer.save()
            # token, create = Token.objects.get_or_create(user=save_user)
            # user_id = Consumer.objects.get(user=save_user).id
            # data = {
            #     'token': token.key,
            #     'username': save_user.username,
            #     'email': save_user.email,
            #     'user_id': user_id
            # }
            # return Response(data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ProfileSingleView(generics.RetrieveDestroyAPIView):
    queryset = Consumer.objects.all()
    serializer_class = ProfileSerializer


class ProfileListView(generics.ListAPIView):
    queryset = Consumer.objects.all()
    serializer_class = ProfileSerializer