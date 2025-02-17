from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializer import *
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class CustomLogInView(generics.ListAPIView):
    pass


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            save_user = serializer.save()
            token, create = Token.objects.get_or_create(user=save_user)
            user_id = save_user.id
            data = {
                'token': token.key,
                'username': save_user.username,
                'email': save_user.email,
                'user_id': user_id
            }
            return Response(data, status.HTTP_201_CREATED)
        else: 
            data = serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)