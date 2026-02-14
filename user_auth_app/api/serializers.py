from rest_framework import serializers
from profile_app.models import UserProfile
from user_auth_app.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.
    Provides a basic representation of user data including username, 
    email, password, and account type.
    """
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "type"]


class RegistrationsSerializer(serializers.ModelSerializer):
    """
    Serializer for handling new user registrations.
    Includes logic for password confirmation, user creation, and 
    the automatic generation of an associated UserProfile.
    """
    repeated_password = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    type = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "repeated_password", "type"]
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def save(self):
        """
        Creates a new CustomUser and an accompanying UserProfile.
        Validates that both password fields match, hashes the password 
        using set_password(), and triggers profile creation.
        """
        pw = self.validated_data["password"]
        repeated_pw = self.validated_data["repeated_password"]

        if pw != repeated_pw:
            raise serializers.ValidationError(
                {"error": "Passwords do not match"}
            )

        account = CustomUser(
            email=self.validated_data["email"],
            username=self.validated_data["username"],
            type=self.validated_data["type"],
        )
        
        account.set_password(pw)
        account.save()
        UserProfile.objects.create(user=account)

        return account

    def validate_email(self, value):
        """
        Ensures the uniqueness of the email address within the platform.
        Checks the database for existing records to prevent duplicate registrations.
        """
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exists"
            )
        return value