from rest_framework import serializers
from order_app.models import *
from offer_app.models import OfferDetail

class OrderSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='offer_detail.title', read_only=True)
    revisions = serializers.IntegerField(source='offer_detail.revisions', read_only=True)
    delivery_time_in_days = serializers.IntegerField(source='offer_detail.delivery_time_in_days', read_only=True)
    price = serializers.IntegerField(source='offer_detail.price', read_only=True)
    offer_type = serializers.CharField(source='offer_detail.offer_type', read_only=True)
    offer_detail_id = serializers.PrimaryKeyRelatedField(
        queryset = OfferDetail.objects.all(),
        write_only = True,
        source = 'offer_detail'
    )
    class Meta:
        model = Order
        fields = ['id', 'revisions', 'title', 'delivery_time_in_days', 'price', 'offer_type', 'status', 'created_at', 'updated_at', 'offer_detail_id']