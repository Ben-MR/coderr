from rest_framework import viewsets, status
from offers_app.api.serializer import OfferDetailSerializer, OfferSerializer, OfferReadSerializer
from offers_app.models import Offer, OfferDetail


class OffersViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return OfferSerializer
        
        return OfferReadSerializer


class OffersDetailViewset(viewsets.ModelViewSet):
    queryset = OfferDetail.objects.all()  
    serializer_class = OfferDetailSerializer