from django.urls import path
from .views import OrderCompletedCountViewSet, OrderCountViewSet, OrdersViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'orders', OrdersViewSet, basename="orders")
router.register(r'order-count', OrderCountViewSet, basename="order-count")
router.register(r'completed-order-count', OrderCompletedCountViewSet, basename="completed-order-count")
urlpatterns = router.urls