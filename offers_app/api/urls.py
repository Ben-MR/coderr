from django.urls import path
from .views import OffersViewSet, OffersDetailViewset
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'', OffersViewSet, basename="offers")
router.register(r'offerdetails', OffersDetailViewset, basename="offerdetails")
urlpatterns = router.urls