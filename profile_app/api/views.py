from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from profile_app.api.permissions import IsOwnProfile
from profile_app.models import UserProfile
from .serializers import UserProfileDetailSerializer, UserProfileUpdateSerializer, UserProfileListCustomerTypSerializer, UserProfileListBusinessTypSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()    
    permission_classes = [IsAuthenticated]

    serializer_class = UserProfileDetailSerializer
    serializer_detail_class = UserProfileDetailSerializer
    serializer_update_class = UserProfileUpdateSerializer

    def get_queryset(self):
        user = self.request.user
        return UserProfile.objects.all()
        
    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.serializer_detail_class
        if self.action in ["update", "partial_update"]:
            return self.serializer_update_class
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            return [IsAuthenticated(), IsOwnProfile()]
        return super().get_permissions()
    
    @action(detail=False, methods=["get"], url_path="customer")
    def customer_type_list(self, request):
        requested_profiles = UserProfile.objects.filter(user__type="customer")

        serializer = UserProfileListCustomerTypSerializer(requested_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["get"], url_path="business")
    def business_type_list(self, request):
        requested_profiles = UserProfile.objects.filter(user__type="business")

        serializer = UserProfileListBusinessTypSerializer(requested_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

