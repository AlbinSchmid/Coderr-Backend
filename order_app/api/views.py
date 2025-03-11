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

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [SellerForPatchOrStaffForDelete]

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = Order.objects.filter(pk=pk).first()

        if obj is None:
            raise OrderNotFound
        return super().get_object()
