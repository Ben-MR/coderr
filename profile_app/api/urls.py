from django.urls import path
from .views import UserProfileViewSet, UserProfilesViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'profile', UserProfileViewSet, basename="profile")
router.register(r'profiles', UserProfilesViewSet, basename="profiles")
urlpatterns = router.urls