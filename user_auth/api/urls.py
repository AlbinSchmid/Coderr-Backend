from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/', CustomLogInView.as_view(), name='log-in'),
    path('registration/', RegistrationView.as_view(), name='registration'),
]