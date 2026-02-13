from rest_framework import serializers

class BaseInfoSerializer(serializers.Serializer):
    review_count = serializers.IntegerField()
    average_rating = serializers.DecimalField(decimal_places=1, max_digits=5, coerce_to_string=False)
    business_profile_count = serializers.IntegerField()
    offer_count = serializers.IntegerField()

    class Meta:
        fields = ["review_count", "average_rating", "business_profile_count", "offer_count"]
