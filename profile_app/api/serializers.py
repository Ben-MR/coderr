from rest_framework import serializers
from profile_app.models import UserProfile

class UserProfileListCustomerTypSerializer(serializers.ModelSerializer):
    """
    Serializer for a simplified customer profile view.
    Retrieves basic information by mapping fields from the related User model 
    to the profile representation.
    """
    user=serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True) #Wenn leer nicht null sondern string
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    file = serializers.ImageField(source="ImageField", read_only=True)
    uploaded_at = serializers.DateTimeField(source="user.date_joined", read_only=True)

    class Meta:
        model = UserProfile
        fields = ["user", "username", "first_name", "last_name", "file", "uploaded_at", "type"]
    
     

class UserProfileListBusinessTypSerializer(serializers.ModelSerializer):
    """
    Serializer for a professional business profile view.
    Extends the basic profile with business-specific details such as 
    location, contact number, description, and working hours.
    """
    user=serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    file = serializers.ImageField(source="ImageField", read_only=True)
    location = serializers.SerializerMethodField(read_only=True)
    tel = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    working_hours = serializers.SerializerMethodField(read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    class Meta:
        model = UserProfile 
        fields = ["user", "username", "first_name", "last_name", "file", "location", "tel", "description", "working_hours", "type"]

    def get_location(self, obj):
        return obj.location or ""

    def get_tel(self, obj):
        return obj.tel or ""
    
    def get_description(self, obj):
        return obj.description or ""
    
    def get_working_hours(self, obj):
        return obj.working_hours or ""

class UserProfileDetailSerializer(serializers.ModelSerializer):
    """
    Comprehensive serializer for full user profile details.
    Aggregates all relevant user and profile data, including account metadata 
    like email and the registration date.
    """
    user=serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    created_at = serializers.DateTimeField(source="user.date_joined", read_only=True)
    file = serializers.ImageField(source="ImageField", read_only=True)
    location = serializers.SerializerMethodField(read_only=True)
    tel = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    working_hours = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserProfile
        fields = ["user", "username", "first_name", "last_name", "file", "location", "tel", "description", "working_hours", "type", "email", "created_at"]

    def get_location(self, obj):
        return obj.location or ""

    def get_tel(self, obj):
        return obj.tel or ""
    
    def get_description(self, obj):
        return obj.description or ""
    
    def get_working_hours(self, obj):
        return obj.working_hours or ""
    
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer to handle updates for user profiles.
    Supports writable fields from both the Profile model and the nested 
    User model (first name, last name, and email).
    """
    user = serializers.CharField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    type = serializers.CharField(source="user.type", read_only=True)
    created_at = serializers.DateTimeField(source="user.date_joined", read_only=True)
    file = serializers.ImageField(source="ImageField", read_only=True)
    class Meta:
        model = UserProfile
        fields = ["user", "username", "first_name", "last_name", "file", "location", "tel", "description", "working_hours", "type", "email", "created_at"]

    def update(self, instance, validated_data):
        """
        Custom update method to synchronize data across two models.
        Updates the primary User instance first before applying changes 
        to the UserProfile instance.
        """
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