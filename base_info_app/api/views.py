from rest_framework import viewsets
from rest_framework.response import Response
from base_info_app.api.serializer import BaseInfoSerializer
from rest_framework.permissions import IsAuthenticated
from offers_app.models import Offer
from offers_app.tests import User
from reviews_app.models import Reviews
from django.db.models import Avg

class BaseInfoViewSet(viewsets.ModelViewSet):
    """
    A ViewSet that provides global platform statistics.

    This ViewSet overrides the standard list method to aggregate data 
    from different models (Reviews, Users, Offers) and returns a 
    summary instead of a simple model list.
    """
    queryset = Reviews.objects.all()   
    serializer_class = BaseInfoSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        """
        Calculates and returns a set of platform-wide metrics.
        
        The data includes:
        - Total number of reviews
        - Weighted average of all star ratings
        - Total count of registered business users
        - Total number of service offers currently available
        """
        data = {
            "review_count": Reviews.objects.count(),
            "average_rating": Reviews.objects.aggregate(Avg('rating'))['rating__avg'] or 0,
            "business_profile_count": User.objects.filter(type = 'business').count(),
            "offer_count": Offer.objects.count(),
        }
        serializer = BaseInfoSerializer(data)

        return Response(serializer.data)
        

   