from django.contrib import admin
from django.urls import path, include
from .view import *

urlpatterns = [
    path('offers/', OfferListView.as_view(), name='offers'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offer-details'),
    path('offerdetails/<int:pk>/', OfferDetailsListView.as_view(), name='offerdetail-detail')
]
