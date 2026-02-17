from django.urls import path, include
from .views import UserProfileViewSet, UserProfilesViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename="profile")
router.register(r'profiles', UserProfilesViewSet, basename="profiles")
urlpatterns = [
    path('', include(router.urls)),
]