from django.urls import path
from .views import UserProfileViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'', UserProfileViewSet, basename="profile")
urlpatterns = router.urls