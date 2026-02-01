from rest_framework import serializers
from profile_app.models import UserProfile

class UserProfileListSerializer(serializers.ModelSerializer):
    pass

class UserProfileDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    joined_date = serializers.DateTimeField(source="user.date_joined", read_only=True)
    class Meta:
        model = UserProfile
        fields = ["id", "username", "first_name", "last_name", "ImageField", "location", "tel", "description", "working_hours", "type", "email", "joined_date"]

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    pass