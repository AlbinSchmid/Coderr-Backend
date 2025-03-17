from rest_framework import generics
from order_app.models import *
from .permissions import *
from .serializers import *
from offer_app.models import OfferDetail
from rest_framework.response import Response
from user_auth.api.permissions import IsAuthenticated


class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [ConsumerForPostOrAuthenticated]

    def perform_create(self, serializer):
        user_id = OfferDetail.objects.select_related('offer__user').values_list('offer__user__id', flat=True).first()
        if user_id:
            business_user = User.objects.get(id=user_id)
        else:
            business_user = None 
        serializer.save(customer_user=self.request.user, business_user=business_user)


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


class OrderCountView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        seller = Seller.objects.filter(user_id=user_id)

        if seller:
            order_count = Order.objects.filter(offer_detail__offer__user__id=user_id, status='in_progress').count()
            return Response({"order_count": order_count})
        raise UserSellerNotFound
    

class CompletedOrderCount(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        seller = Seller.objects.filter(user_id=user_id)
        if seller:
            order_count = Order.objects.filter(offer_detail__offer__user__id=user_id, status='completed').count()
            return Response({"completed_order_count": order_count})
        raise UserSellerNotFound
    
