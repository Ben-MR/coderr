from rest_framework import serializers
from offers_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferDetail
        fields = ["id", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type"]

class OfferSerializer(serializers.ModelSerializer):

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "title",
            "image",
            "description",
            "min_price",
            "min_delivery_time",
            "details",
        ]
        read_only_fields = ["min_price", "min_delivery_time"]

    def create(self, validated_data):
        details_list = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)

        for item in details_list:
            OfferDetail.objects.create(offer = offer, **item)
        return offer


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='offerdetails-detail', 
        read_only=True
    )
    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

class OfferReadSerializer(serializers.ModelSerializer):
    details = OfferDetailLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "title",
            "image",
            "description",
            "min_price",
            "min_delivery_time",
            "details",
        ]
        read_only_fields = ["min_price", "min_delivery_time"]