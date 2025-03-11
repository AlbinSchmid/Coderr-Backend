from rest_framework import serializers
from order_app.models import *
from offer_app.models import OfferDetail
from .exeptions import OfferDetailNotExist

class OrderSerializer(serializers.ModelSerializer):
    business_user = serializers.CharField(source='offer_detail.offer.user.id', read_only=True)
    title = serializers.CharField(source='offer_detail.title', read_only=True)
    revisions = serializers.IntegerField(source='offer_detail.revisions', read_only=True)
    delivery_time_in_days = serializers.IntegerField(source='offer_detail.delivery_time_in_days', read_only=True)
    price = serializers.IntegerField(source='offer_detail.price', read_only=True)
    offer_type = serializers.CharField(source='offer_detail.offer_type', read_only=True)
    features = serializers.JSONField(source='offer_detail.features', read_only=True)
    offer_detail_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'business_user', 'customer_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at', 'offer_detail_id']
        read_only_fields = ['customer_user']

    def validate_offer_detail_id(self, value):
        if not OfferDetail.objects.filter(id=value).exists():
            raise OfferDetailNotExist
        return value
    
    def create(self, validated_data):
        offer_detail_id = validated_data.pop('offer_detail_id')
        offer_detail = OfferDetail.objects.get(id=offer_detail_id)
        return Order.objects.create(offer_detail=offer_detail, **validated_data)
    

class OrderCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'