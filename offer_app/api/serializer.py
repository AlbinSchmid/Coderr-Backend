from rest_framework import serializers
from offer_app.models import *
from .exeptions import BadRequest


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'offer_type', 'features']


class OfferDetailsHyperlinkedSerializer(serializers.HyperlinkedModelSerializer, OfferDetailSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'url']


class OfferListBigDetailsSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Offer
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None

        lowest_price = min(item['price'] for item in details_data) if details_data else 0
        lowest_delivery_time = min(item['delivery_time_in_days'] for item in details_data) if details_data else 0
        
        offer = Offer.objects.create(user=user, **validated_data, min_price=lowest_price, min_delivery_time=lowest_delivery_time)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer
    
    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None) 

        if details_data is not None:
            for detail_data in details_data:
                offer_type = detail_data.get('offer_type') 
                detail = instance.details.filter(offer_type=offer_type).first()

                if detail is not None:
                    OfferDetail.objects.filter(id=detail.id).update(**detail_data)
                else: 
                    raise BadRequest
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    
class OfferListSmallDetailsSerializer(serializers.ModelSerializer):
    details = OfferDetailsHyperlinkedSerializer(many=True)
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Offer
        fields = '__all__'
        read_only_fields = ['user']

