from django.urls import path
from .views import BaseInfoViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'base-info', BaseInfoViewSet, basename="offers")
urlpatterns = router.urls