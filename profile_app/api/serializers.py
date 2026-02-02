from rest_framework import serializers
from profile_app.models import UserProfile

class UserProfileListCustomerTypSerializer(serializers.ModelSerializer):
    user=serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    file = serializers.ImageField(source="ImageField", read_only=True)
    class Meta:
        model = UserProfile
        fields = ["user", "username", "first_name", "last_name", "file", "type"]

class UserProfileListBusinessTypSerializer(serializers.ModelSerializer):
    user=serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    file = serializers.ImageField(source="ImageField", read_only=True)
    class Meta:
        model = UserProfile
        fields = ["user", "username", "first_name", "last_name", "file", "location", "tel", "description", "working_hours", "type"]

class UserProfileDetailSerializer(serializers.ModelSerializer):
    user=serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    created_at = serializers.DateTimeField(source="user.date_joined", read_only=True)
    file = serializers.ImageField(source="ImageField", read_only=True)
    class Meta:
        model = UserProfile
        fields = ["user", "username", "first_name", "last_name", "file", "location", "tel", "description", "working_hours", "type", "email", "created_at"]

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    class Meta:
        model = UserProfile
        fields = ["first_name", "last_name", "location", "tel", "description", "working_hours", "email"]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        
        if user_data:
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.email = user_data.get('email', user.email)
            user.save()

        instance.location = validated_data.get('location', instance.location)
        instance.tel = validated_data.get('tel', instance.tel)
        instance.description = validated_data.get('description', instance.description)
        instance.working_hours = validated_data.get('working_hours', instance.working_hours)

        instance.save()

        return instance