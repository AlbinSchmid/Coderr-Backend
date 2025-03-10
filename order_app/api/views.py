from rest_framework import generics
from order_app.models import *
from .permissions import *
from .serializers import *
from offer_app.models import OfferDetail


class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [ConsumerForPostOrAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer_user=self.request.user)
    
        # serializer.save(customer_user=self.request.user)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
