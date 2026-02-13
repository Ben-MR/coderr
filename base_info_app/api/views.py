from rest_framework import viewsets
from rest_framework.response import Response
from base_info_app.api.serializer import BaseInfoSerializer
from rest_framework.permissions import IsAuthenticated
from offers_app.models import Offer
from offers_app.tests import User
from reviews_app.models import Reviews
from django.db.models import Avg

class BaseInfoViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()   
    serializer_class = BaseInfoSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        data = {
            "review_count": Reviews.objects.count(),
            "average_rating": Reviews.objects.aggregate(Avg('rating'))['rating__avg'] or 0,
            "business_profile_count": User.objects.filter(type = 'business').count(),
            "offer_count": Offer.objects.count(),
        }
        serializer = BaseInfoSerializer(data)

        return Response(serializer.data)
        

   