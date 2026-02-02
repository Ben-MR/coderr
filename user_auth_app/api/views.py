from rest_framework.authtoken.models import Token as AuthToken
from rest_framework import generics
from user_auth_app.models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegistrationsSerializer
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status


class CustomUserList(generics.ListCreateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CustomUserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a single user profile.

    - GET: Returns one UserProfile by primary key.
    - PUT/PATCH: Updates the profile.
    - DELETE: Removes the profile.

    Notes:
    - Access control depends on your global DRF settings or additional
      permission_classes added here.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class RegistrationsView(APIView):
    """
    User registration endpoint.

    Accepts registration data, creates a new user account, and returns
    a DRF auth token plus basic user information.

    Expected request fields (based on RegistrationsSerializer):
    - username
    - email
    - password
    - repeated_password
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Register a new user.

        On success:
        - Creates the user (password is hashed in the serializer)
        - Creates or fetches a DRF Token
        - Returns: token, username, email, user_id

        On validation error:
        - Returns serializer errors

        Returns:
            Response: 200 with token payload or validation errors.
        """
        serializer = RegistrationsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        saved_account = serializer.save()
        token, _ = Token.objects.get_or_create(user=saved_account)

        return Response(
            {
                "token": token.key,
                "username": saved_account.username,
                "email": saved_account.email,
                "user_id": saved_account.id,
            },
            status=200,
        )


class CustomLogin(ObtainAuthToken):

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        # Frontend sends email -> DRF ObtainAuthToken expects username
        # if "username" not in data and "email" in data:
        #     data["username"] = data["email"]

        serializer = self.serializer_class(data=data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            },
            status=200,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # request.auth is the Token instance under TokenAuthentication
        if request.auth is not None:
            request.auth.delete()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)


# class EmailCheckView(APIView):
#     """
#     Endpoint to check whether a given email address exists.

#     - GET /...?email=someone@example.com
#     - Returns user details (id/email/username) if present, otherwise exists=False.
#     """

#     serializer_class = EmailCheckSerializer

#     def get(self, request):
#         """
#         Validate the email query parameter and return existence info.

#         Query params:
#             email (str): Email address to check.

#         Returns:
#             Response: Serialized existence information.
#         """
#         email = request.query_params.get("email", "")

#         serializer = self.serializer_class(data={"email": email})
        
#         if serializer.is_valid(raise_exception=True):
#             return Response(serializer.to_representation(serializer.validated_data))
#         return Response(serializer.errors, status=404)
