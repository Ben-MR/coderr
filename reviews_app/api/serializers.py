from rest_framework import serializers
from reviews_app.models import Reviews
from rest_framework.validators import UniqueTogetherValidator

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Reviews model.
    
    Handles the serialization of review data including the associated business user,
    the rating, and the description. The 'reviewer' field is set to read-only 
    as it is automatically assigned to the authenticated user during creation.
    """
  
    class Meta:
        model = Reviews
        fields = ['id', 'business_user', 'reviewer',  'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['reviewer']