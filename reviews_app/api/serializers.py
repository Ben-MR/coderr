from rest_framework import serializers
from reviews_app.models import Reviews
from rest_framework.validators import UniqueTogetherValidator

class ReviewSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Reviews
        fields = ['id', 'business_user', 'reviewer',  'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['reviewer']


       




