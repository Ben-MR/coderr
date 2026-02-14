from rest_framework.authtoken.models import Token as AuthToken
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from user_auth_app.models import CustomUser
from .serializers import CustomUserSerializer
from .serializers import RegistrationsSerializer



class CustomUserList(generics.ListCreateAPIView):
    """
    API view to retrieve a list of all users or create a new user.
    Utilizes standard generic ListCreateAPIView for core user management.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CustomUserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific user by their ID.
    Provides standard RESTful endpoints for individual user administration.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class RegistrationsView(APIView):
    """
    Endpoint for public user registration.
    
    Processing steps:
    1. Validates input data via RegistrationsSerializer.
    2. Creates a new CustomUser account.
    3. Generates an authentication token for the new user.
    4. Returns user details and the token for immediate login.
    """
    permission_classes = [AllowAny]

    def post(self, request):
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
    """
    Custom login view extending the standard ObtainAuthToken.
    
    Verifies credentials and returns a response containing the 
    authentication token along with essential user profile information 
    (username, email, and ID) for the frontend client.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
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
    """
    Endpoint for user logout.
    
    Requires an authenticated request. Upon invocation, it identifies 
    and deletes the current authentication token from the database, 
    effectively invalidating the session.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.auth is not None:
            request.auth.delete()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)