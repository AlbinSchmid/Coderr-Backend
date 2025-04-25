from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from offer_app.models import *
from .serializer import *
from .permissions import *
from .pagination import *
from user_auth.api.permissions import IsAuthenticated

class OfferListView(generics.ListCreateAPIView):
    """
    View to list and create offers.
    """
    queryset = Offer.objects.all()
    permission_classes = [SellerUserCreateOrReadOnly]
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['updated_at', 'min_price']
    search_fields = ['title', 'description']

    def get_queryset(self):
        """
        Optionally restricts the returned offers to a given user,
        by filtering against a `creator_id` query parameter in the URL.
        """
        queryset = Offer.objects.all()
        creator_id_param = self.request.query_params.get('creator_id', None)
        max_delivery_time_param = self.request.query_params.get('max_delivery_time', None)
        min_price = self.request.query_params.get('min_price', None)

        if creator_id_param and creator_id_param.isdigit():
            queryset = queryset.filter(user__id=creator_id_param)
        elif creator_id_param != '' and creator_id_param is not None:
            raise IncorrectParams

        if max_delivery_time_param and max_delivery_time_param.isdigit():
            queryset = queryset.filter(min_delivery_time__lte=max_delivery_time_param)
        elif max_delivery_time_param != '' and max_delivery_time_param is not None:
            raise IncorrectParams

        if min_price and min_price.isdigit():
            queryset = queryset.filter(min_price__gte=min_price)
        elif min_price != '' and min_price is not None:
            raise IncorrectParams
        return self.filter_queryset(queryset) 

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the request method.
        """
        if self.request.method == 'POST':
            return OfferListBigDetailsSerializer
        return OfferListSmallDetailsSerializer

class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete an offer.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferListSmallDetailsSerializer
    permission_classes = [OwnerPatchAndDeleteOrIsAuthenticated]

    def get_object(self):
        """
        Retrieve the offer object based on the provided primary key (pk).
        """
        pk = self.kwargs.get('pk')
        obj = Offer.objects.filter(pk=pk).first()
        
        if self.request.user and self.request.user.is_authenticated:
            if obj is None:
                raise OfferNotFound
            return super().get_object()
        raise Unauthorized

    
    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the request method.
        """
        if self.request.method == 'PATCH':
            return OfferListBigDetailsSerializer
        return OfferListSmallDetailsSerializer

class OfferDetailsListView(generics.RetrieveAPIView):
    """
    View to retrieve the details of a specific offer.
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [Authenticated]

    def get_object(self):
        """
        Retrieve the offer detail object based on the provided primary key (pk).
        """
        pk = self.kwargs.get('pk')
        obj = OfferDetail.objects.filter(pk=pk).first()
        
        if obj is None:
            raise OfferNotFound
        return super().get_object()