from rest_framework import generics
from order_app.models import *
from .permissions import *
from .serializers import *
from offer_app.models import OfferDetail
from rest_framework.response import Response
from user_auth.api.permissions import IsAuthenticated
from user_auth.models import Seller


class OrderListView(generics.ListCreateAPIView):
    """
    View to list and create orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [ConsumerForPostOrAuthenticated]

    def perform_create(self, serializer):
        """
        Save the order with the customer user and business user.
        """
        offer_detail_id = self.request.data.get('offer_detail_id')
        offer_detail_user = OfferDetail.objects.filter(id=offer_detail_id).select_related('offer__user').first()
        business_user = offer_detail_user.offer.user
        serializer.save(customer_user=self.request.user, business_user=business_user)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete an order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [SellerForPatchOrStaffForDelete]

    def get_object(self):
        """
        Retrieve the order object based on the provided primary key (pk).
        """
        pk = self.kwargs.get('pk')
        obj = Order.objects.filter(pk=pk).first()
            
        if obj is None:
            raise OrderNotFound
        return super().get_object()


class OrderCountView(generics.ListAPIView):
    """
    View to count the number of orders for a specific seller.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Get the count of orders for a specific seller.
        """
        user_id = kwargs.get('pk')
        seller = Seller.objects.filter(user_id=user_id)

        if seller:
            order_count = Order.objects.filter(offer_detail__offer__user__id=user_id, status='in_progress').count()
            return Response({"order_count": order_count})
        raise UserSellerNotFound
    

class CompletedOrderCount(generics.ListAPIView):
    """
    View to count the number of completed orders for a specific seller.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Get the count of completed orders for a specific seller.
        """
        user_id = kwargs.get('pk')
        seller = Seller.objects.filter(user_id=user_id)
        if seller:
            order_count = Order.objects.filter(offer_detail__offer__user__id=user_id, status='completed').count()
            return Response({"completed_order_count": order_count})
        raise UserSellerNotFound
    
