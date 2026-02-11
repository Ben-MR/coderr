from django.urls import path
from .views import ReviewsViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'reviews', ReviewsViewSet, basename="reviews")
urlpatterns = router.urls