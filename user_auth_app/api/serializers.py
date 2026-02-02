from rest_framework import serializers
from profile_app.models import UserProfile
from user_auth_app.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):


    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "type"]


class RegistrationsSerializer(serializers.ModelSerializer):

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
        Ensure the email address is unique.

        Args:
            value (str): Email address provided during registration.

        Raises:
            ValidationError: If a user with this email already exists.

        Returns:
            str: The validated email value.
        """
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exists"
            )
        return value


# class EmailCheckSerializer(serializers.Serializer):
#     """
#     Serializer used to check whether an email address
#     is already registered.

#     Returns basic user information if the email exists.
#     """

#     email = serializers.EmailField()
#     exists = serializers.BooleanField(read_only=True)
#     id = serializers.IntegerField(read_only=True)
#     first_name = serializers.CharField(read_only=True)

#     def to_representation(self, data):
#         """
#         Return information about the user associated with the given email.

#         If a user exists:
#         - return id, email, and username

#         If no user exists:
#         - return exists = False
#         """
#         email = data["email"]
#         user = User.objects.filter(email__iexact=email).first()

#         if user:
#             return {
#                 "id": user.id,
#                 "email": user.email,
#                 "fullname": user.first_name,
#             }

#         return {"exists": False}
