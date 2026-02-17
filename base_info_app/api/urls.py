from django.urls import path, include
from .views import BaseInfoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'base-info', BaseInfoViewSet, basename="base-info")

urlpatterns = [
    path('', include(router.urls)),
]