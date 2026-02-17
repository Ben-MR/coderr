from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from profile_app.api.permissions import IsOwnProfile
from profile_app.models import UserProfile
from .serializers import UserProfileDetailSerializer, UserProfileUpdateSerializer, UserProfileListCustomerTypSerializer, UserProfileListBusinessTypSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing the authenticated user's profile.
    
    Provides detailed views and update capabilities. It dynamically switches 
    serializers for retrieval and update actions and ensures that only the 
    profile owner can perform modifications.
    """
    queryset = UserProfile.objects.all()    
    permission_classes = [IsAuthenticated]

    serializer_class = UserProfileDetailSerializer
    serializer_detail_class = UserProfileDetailSerializer
    serializer_update_class = UserProfileUpdateSerializer

    def get_queryset(self):
        """
        Returns the queryset of UserProfiles.
        Currently returns all profiles, but provides a hook for future 
        user-specific filtering.
        """
        user = self.request.user
        return UserProfile.objects.all()
        
    def get_serializer_class(self):
        """
        Selects the appropriate serializer based on the current action.
        - retrieve: Returns detailed profile data.
        - update/partial_update: Returns the update-optimized serializer.
        """
        if self.action == "retrieve":
            return self.serializer_detail_class
        if self.action in ["update", "partial_update"]:
            return self.serializer_update_class
        return super().get_serializer_class()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        Updates and partial updates are restricted to the owner of the profile.
        """
        if self.action in ["update", "partial_update"]:
            return [IsAuthenticated(), IsOwnProfile()]
        return super().get_permissions()  
    
    def get_object(self):
        """
        Retrieves the profile based on the User's ID (from the URL).
        This prevents mismatches if Profile IDs and User IDs are not identical.
        """
        pk = self.kwargs.get('pk')
        return get_object_or_404(UserProfile, user__id=pk)
    

class UserProfilesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only ViewSet for browsing user profiles.
    
    Includes custom actions to filter profiles based on user types 
    (Customer or Business) with specialized list serializers for each type.
    """
    queryset = UserProfile.objects.all()    
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileDetailSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            instance = self.get_object()
            if instance.user.type == "business":
                return UserProfileListBusinessTypSerializer
            return UserProfileListCustomerTypSerializer
        return UserProfileDetailSerializer

    @action(detail=False, methods=["get"], url_path="customer")
    def customer_type_list(self, request):
        """
        Custom action to retrieve a list of all profiles belonging 
        to users with the 'customer' type.
        """
        requested_profiles = UserProfile.objects.filter(user__type="customer")

        serializer = UserProfileListCustomerTypSerializer(requested_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["get"], url_path="business")
    def business_type_list(self, request):
        """
        Custom action to retrieve a list of all profiles belonging 
        to users with the 'business' type.
        """
        requested_profiles = UserProfile.objects.filter(user__type="business")

        serializer = UserProfileListBusinessTypSerializer(requested_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)