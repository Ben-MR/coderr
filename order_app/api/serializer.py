from rest_framework import serializers
from order_app.models import Order

class OderSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing and creating orders.
    
    Uses ReadOnlyFields with source mapping to pull detailed information 
    (title, price, delivery time, etc.) from the associated OfferDetail.
    The customer and business users are linked automatically and treated as read-only.
    """
    title = serializers.ReadOnlyField(source='offer_detail.offer.title')
    revisions = serializers.ReadOnlyField(source='offer_detail.revisions')
    delivery_time_in_days = serializers.ReadOnlyField(source='offer_detail.delivery_time_in_days')
    price = serializers.ReadOnlyField(source='offer_detail.price')
    features = serializers.ReadOnlyField(source='offer_detail.features')
    offer_type = serializers.ReadOnlyField(source='offer_detail.offer_type')
    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)
    

    class Meta:
        model = Order
        fields = [
            'id', 'business_user', 'customer_user',  'title', 
            'revisions', 'delivery_time_in_days', 'price', 'features', "offer_type", 'status', 'created_at'
        ]

class OrderUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer optimized for updating an existing order's progress.
    
    Maintains visibility of all order details while specifically 
    allowing modification of the 'status' field.
    """
    title = serializers.ReadOnlyField(source='offer_detail.offer.title')
    revisions = serializers.ReadOnlyField(source='offer_detail.revisions')
    delivery_time_in_days = serializers.ReadOnlyField(source='offer_detail.delivery_time_in_days')
    price = serializers.ReadOnlyField(source='offer_detail.price')
    features = serializers.ReadOnlyField(source='offer_detail.features')
    offer_type = serializers.ReadOnlyField(source='offer_detail.offer_type')
    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Order
        fields = [
            'id', 'business_user', 'customer_user',  'title', 
            'revisions', 'delivery_time_in_days', 'price', 'features', "offer_type", 'status', 'created_at'
        ]

    def update(self, instance, validated_data):
        """
        Updates the order instance.
        Primarily focuses on transitioning the 'status' attribute 
        based on the validated data provided by the business user.
        """
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance