from django.urls import path
from .views import OrderCompletedCountViewSet, OrderCountViewSet, OrdersViewSet
from rest_framework import routers
from django.urls import path, include 

router = routers.DefaultRouter() 
router.register(r'orders', OrdersViewSet, basename="orders")
router.register(r'order-count', OrderCountViewSet, basename="order-count")
router.register(r'completed-order-count', OrderCompletedCountViewSet, basename="completed-order-count")

urlpatterns = [
    path('', include(router.urls)),
]