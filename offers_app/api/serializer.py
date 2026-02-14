from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from django.db.models import Max, Min


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the specific pricing tiers of an offer.
    Handles fields like title, revisions, delivery time, and price 
    for basic, standard, or premium versions of a service.
    """
    class Meta:
        model = OfferDetail
        fields = ["id", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type"]

class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer used for creating new service offers.
    Handles the primary offer data and includes nested creation of 
    multiple OfferDetail instances.
    """
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
        """
        Custom create method to handle nested OfferDetail objects.
        Links the new offer to the authenticated user and creates 
        associated detail tiers in the database.
        """
        user = self.context['request'].user        
        details_list = validated_data.pop('details')    
        offer = Offer.objects.create(user=user, **validated_data)

        for item in details_list:
            OfferDetail.objects.create(offer=offer, **item)
            
        return offer


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    """
    A lightweight serializer for OfferDetails that provides a 
    hyperlinked identity to the detail's specific endpoint.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='offerdetails-detail', 
        read_only=True
    )
    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

class OfferReadSerializer(serializers.ModelSerializer):
    """
    Serializer for list views of offers.
    Provides calculated fields for minimum price and minimum delivery time 
    while linking to detail tiers via URLs.
    """
    details = OfferDetailLinkSerializer(many=True, read_only=True)
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "min_price",
            "min_delivery_time",
            "details",
        ]
        read_only_fields = ["min_price", "min_delivery_time"]
  
    def get_min_delivery_time(self, obj):
        """
        Calculates the minimum delivery time among all associated 
        pricing tiers for a specific offer.
        """
        result = obj.details.aggregate(Min("delivery_time_in_days"))
        return result["delivery_time_in_days__min"] or 0
    
class OfferSingleReadSerializer(serializers.ModelSerializer):
    """
    Serializer for the detailed retrieval of a single offer.
    Returns comprehensive information including the associated owner 
    and timestamps.
    """
    details = OfferDetailLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = ["id", "user", "title", "image", "description", "created_at",  "updated_at", "details"]


class OfferUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer to handle updates of existing offers and their nested details.
    Allows modification of the main offer body and updates corresponding 
    pricing tiers based on their type.
    """
    details = OfferDetailSerializer(many=True)
    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]
    
    
    def update(self, instance, validated_data):
        """
        Custom update logic to sync nested OfferDetail data.
        Updates the main instance first, then iterates through detail 
        data to update associated tiers matching the 'offer_type'.
        """
        details_data = validated_data.pop('details', [])
        instance = super().update(instance, validated_data)        
        for data in details_data:
            instance.details.filter(offer_type=data.get('offer_type')).update(**data)

        return instance