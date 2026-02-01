from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from profile_app.models import UserProfile
from .serializers import UserProfileListSerializer, UserProfileDetailSerializer, UserProfileUpdateSerializer



class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()    

    serializer_list_class = UserProfileListSerializer
    serializer_detail_class = UserProfileDetailSerializer
    serializer_update_class = UserProfileUpdateSerializer

    def get_queryset(self):
        user = self.request.user
        return UserProfile.objects.all()
        
    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.serializer_detail_class
        if self.action == "list":
            return self.serializer_list_class
        if self.action in ["update", "partial_update"]:
            return self.serializer_update_class
        return super().get_serializer_class()

    def get_permissions(self):

        if self.action == "destroy":
            return [IsAuthenticated()]
        return super().get_permissions()
