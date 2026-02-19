from rest_framework import serializers
from offers_app.models import OfferDetail
from order_app.models import Order

class OderSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing and creating orders.
    
    Uses ReadOnlyFields with source mapping to pull detailed information 
    (title, price, delivery time, etc.) from the associated OfferDetail.
    The customer and business users are linked automatically and treated as read-only.
    """
    title = serializers.ReadOnlyField(source='offer_detail.title')
    revisions = serializers.ReadOnlyField(source='offer_detail.revisions')
    delivery_time_in_days = serializers.ReadOnlyField(source='offer_detail.delivery_time_in_days')
    price = serializers.ReadOnlyField(source='offer_detail.price')
    features = serializers.ReadOnlyField(source='offer_detail.features')
    offer_type = serializers.ReadOnlyField(source='offer_detail.offer_type')
    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)
    offer_detail_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Order
        fields = [
            'id', 'business_user', 'customer_user',  'title', 'revisions', 'delivery_time_in_days',
             'price', 'features', "offer_type", 'status', 'created_at', 'updated_at', "offer_detail_id"
        ]

    def validate_offer_detail_id(self, value):
        """
        Validates that offer_detail_id is a strict integer and exists.
        
        - Checks the raw input type to prevent string-to-integer conversion.
        - Verifies that the referenced OfferDetail exists in the database.
        - Raises 400 if validation fails.
        """
        raw_value = self.initial_data.get('offer_detail_id')
        
        if not isinstance(raw_value, int):
            raise serializers.ValidationError("only integer allowed")

        if not OfferDetail.objects.filter(id=value).exists():
            raise serializers.ValidationError("400")
            
        return value

class OrderUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer optimized for updating an existing order's progress.
    
    Maintains visibility of all order details while specifically 
    allowing modification of the 'status' field.
    """
    title = serializers.ReadOnlyField(source='offer_detail.title')
    revisions = serializers.ReadOnlyField(source='offer_detail.revisions')
    delivery_time_in_days = serializers.ReadOnlyField(source='offer_detail.delivery_time_in_days')
    price = serializers.ReadOnlyField(source='offer_detail.price')
    features = serializers.ReadOnlyField(source='offer_detail.features')
    offer_type = serializers.ReadOnlyField(source='offer_detail.offer_type')
    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)
    offer_detail_id = serializers.IntegerField(write_only=True, required=True)
    class Meta:
        model = Order
        fields = [
            'id', 'business_user', 'customer_user',  'title', 
            'revisions', 'delivery_time_in_days', 'price', 'features', "offer_type", 'status', 'created_at', 'updated_at', 'offer_detail_id'
        ]

    def validate_offer_detail_id(self, value):
        """
        Validates the 'offer_detail_id' field to ensure strict data integrity.
        
        - Checks if the raw input (initial_data) is a literal integer to prevent 
          type-coercion errors or server crashes (500) caused by strings.
        - Verifies the existence of the corresponding OfferDetail instance 
          in the database.
        - Raises a 400 ValidationError if the type is invalid or the ID does not exist.
        """
        initial_value = self.initial_data.get('offer_detail_id')        
        if not isinstance(initial_value, int):
            raise serializers.ValidationError("400")            
        if not OfferDetail.objects.filter(id=value).exists():
            raise serializers.ValidationError("400")
            
        return value

    def update(self, instance, validated_data):
        """
        Updates the order instance.
        Primarily focuses on transitioning the 'status' attribute 
        based on the validated data provided by the business user.
        """
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance