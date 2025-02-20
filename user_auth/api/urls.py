from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/', CustomLogInView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/', ProfileListView.as_view(), name='profile'),
    path('profile/<int:pk>/', ProfileSingleView.as_view(), name='profile-detail'),
    path('profile/business/', SellerListView.as_view(), name="seller"),
    path('profile/customer/', ConsumerListView.as_view(), name="consumer")
]