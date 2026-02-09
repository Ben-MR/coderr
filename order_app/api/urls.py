from django.urls import path
from .views import OrdersViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'orders', OrdersViewSet, basename="orders")
#router.register(r'offerdetails', OffersDetailViewset, basename="offerdetails")
urlpatterns = router.urls