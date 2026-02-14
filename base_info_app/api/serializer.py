from rest_framework import serializers

class BaseInfoSerializer(serializers.Serializer):
    """
    Serializer to represent general platform statistics.
    
    This serializer is not bound to a specific model. It is used to 
    aggregate data from multiple sources (Reviews, Profiles, Offers) 
    to provide a summary of the platform's current state.
    """
    review_count = serializers.IntegerField()
    average_rating = serializers.DecimalField(decimal_places=1, max_digits=5, coerce_to_string=False)
    business_profile_count = serializers.IntegerField()
    offer_count = serializers.IntegerField()

    class Meta:
        """
        Metadata for the BaseInfoSerializer.
        Defines the fields to be included in the serialized output.
        """
        fields = ["review_count", "average_rating", "business_profile_count", "offer_count"]
