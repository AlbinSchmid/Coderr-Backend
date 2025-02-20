from rest_framework import serializers
from offer_app.models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'offer_type', 'features']


class OfferSerializer(serializers.ModelSerializer):
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

        offer = Offer.objects.create(user=user, **validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer

