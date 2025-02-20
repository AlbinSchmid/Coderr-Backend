from rest_framework import generics
from offer_app.models import *
from .serializer import *

class OfferListView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

class OfferDetailView(generics.RetrieveDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

class DetailListView(generics.RetrieveDestroyAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer