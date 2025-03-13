from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('reviews/', ReviewListView.as_view(), name='reviews'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review'),
]