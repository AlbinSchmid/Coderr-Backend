from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from offer_app.models import *
from .serializer import *
from .permissions import *
from .pagination import *
from user_auth.api.permissions import IsAuthenticated

class OfferListView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    permission_classes = [SellerUserCreateOrReadOnly]
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['min_price']
    ordering_fields = ['updated_at', 'min_price']
    search_fields = ['title', 'description']

    def get_queryset(self):
        queryset = Offer.objects.all()
        creator_id_param = self.request.query_params.get('creator_id', None)
        max_delivery_time_param = self.request.query_params.get('max_delivery_time', None)

        if creator_id_param:
            queryset = queryset.filter(user__id=creator_id_param)

        if max_delivery_time_param:
            queryset = queryset.filter(min_delivery_time__lte=max_delivery_time_param)

        return self.filter_queryset(queryset) 

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferListBigDetailsSerializer
        return OfferListSmallDetailsSerializer

class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferListSmallDetailsSerializer
    permission_classes = [OwnerPatchAndDeleteOrIsAuthenticated]

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = Offer.objects.filter(pk=pk).first()
        
        if obj is None:
            raise OfferNotFound
        return super().get_object()
    
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return OfferListBigDetailsSerializer
        return OfferListSmallDetailsSerializer

class OfferDetailsListView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [Authenticated]

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = OfferDetail.objects.filter(pk=pk).first()
        
        if obj is None:
            raise OfferNotFound
        return super().get_object()