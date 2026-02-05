from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from django.db.models import Max, Min


class OfferDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferDetail
        fields = ["id", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type"]

class OfferSerializer(serializers.ModelSerializer):
    
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            "title",
            "image",
            "description",
            "details",
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        
        details_list = validated_data.pop('details')    
 
        offer = Offer.objects.create(user=user, **validated_data)

        for item in details_list:
            OfferDetail.objects.create(offer=offer, **item)
            
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
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

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

    def get_min_price(self, obj):
        result = obj.details.aggregate(Min("price"))
        return result["price__min"] or 0
    
    def get_min_delivery_time(self, obj):
        result = obj.details.aggregate(Min("delivery_time_in_days"))
        return result["delivery_time_in_days__min"] or 0
    
class OfferSingleReadSerializer(serializers.ModelSerializer):
    details = OfferDetailLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = ["id", "user", "title", "image", "description", "created_at",  "updated_at", "details"]


class OfferUpdateSerializer(serializers.ModelSerializer):
    
    details = OfferDetailSerializer(many=True)
    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]
    
    
    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', [])
        instance = super().update(instance, validated_data)        
        for data in details_data:
            instance.details.filter(offer_type=data.get('offer_type')).update(**data)

        return instance