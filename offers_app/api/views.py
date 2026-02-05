from rest_framework import viewsets, status
from offers_app.api.permissions import IsOwnOffer
from offers_app.api.serializer import OfferDetailSerializer, OfferSerializer, OfferReadSerializer, OfferSingleReadSerializer, OfferUpdateSerializer
from offers_app.models import Offer, OfferDetail
from rest_framework.permissions import IsAuthenticated


class OffersViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return OfferSerializer
        if self.action == "retrieve":
            return OfferSingleReadSerializer
        if self.action == 'partial_update':
            return OfferUpdateSerializer
        
        return OfferReadSerializer

    def get_permissions(self):
        if self.action in ["destroy", "partial_update"]:
            return [IsAuthenticated(), IsOwnOffer()]
        return super().get_permissions()

class OffersDetailViewset(viewsets.ModelViewSet):
    queryset = OfferDetail.objects.all()  
    serializer_class = OfferDetailSerializer