from rest_framework import serializers

from order_app.models import Order

class OderSerializer(serializers.ModelSerializer):
    offer_detail_id = serializers.IntegerField(write_only=True)
    id = serializers.ReadOnlyField(source='offer_detail.offer_id')
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
            'offer_detail_id', 'id', 'business_user', 'customer_user',  'title', 
            'revisions', 'delivery_time_in_days', 'price', 'features', "offer_type", 'status', 'created_at'
        ]

class OrderUpdateSerializer(serializers.ModelSerializer):
    offer_detail_id = serializers.IntegerField(write_only=True)
    id = serializers.ReadOnlyField(source='offer_detail.offer_id')
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
            'offer_detail_id', 'id', 'business_user', 'customer_user',  'title', 
            'revisions', 'delivery_time_in_days', 'price', 'features', "offer_type", 'status', 'created_at'
        ]

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)

        instance.save()

        return instance
    
    
        




