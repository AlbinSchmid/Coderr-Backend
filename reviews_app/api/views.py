from rest_framework import generics
from rest_framework import filters
from reviews_app.models import *
from .serializers import *
from .permissions import *
from django_filters.rest_framework import DjangoFilterBackend

class ReviewListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [isAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['updated_at', 'rating']

    def get_queryset(self):
        queryset = Review.objects.all()
        reviewer_id_param = self.request.query_params.get('reviewer_id', None)
        business_user_id_param = self.request.query_params.get('business_user_id', None)

        if reviewer_id_param:   
            queryset = queryset.filter(reviewer=reviewer_id_param)

        if business_user_id_param:
            queryset = queryset.filter(business_user=business_user_id_param)
            

        return self.filter_queryset(queryset)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [OwnerForDeleteAndPatch]

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = Review.objects.filter(pk=pk).first()

        if obj is None:
            raise ReviewNotFound
        return super().get_object()