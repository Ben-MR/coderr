from django.urls import path, include
from .views import OffersViewSet, OffersDetailViewset
from rest_framework import routers

router = routers.DefaultRouter() 
router.register(r'offers', OffersViewSet, basename="offers")
router.register(r'offerdetails', OffersDetailViewset, basename="offerdetails")

urlpatterns = [
    path('', include(router.urls)),
]