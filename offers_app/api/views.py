import django_filters
from rest_framework import viewsets, status
from offers_app.api.permissions import IsOwnOffer, IsBusinessUser
from offers_app.api.serializer import OfferDetailSerializer, OfferSerializer, OfferReadSerializer, OfferSingleReadSerializer, OfferUpdateSerializer
from offers_app.models import Offer, OfferDetail
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class OfferFilter(django_filters.FilterSet):
    creator_id = django_filters.NumberFilter(field_name='user__id')
    min_price = django_filters.NumberFilter(field_name='details__price', lookup_expr='gte')
    max_delivery_time = django_filters.NumberFilter(field_name='details__delivery_time_in_days', lookup_expr='lte')

    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price', 'max_delivery_time']


class OffersViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']


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
        if self.action in "create":
            return [IsAuthenticated(), IsBusinessUser()]
        return super().get_permissions()
    
    
    def get_queryset(self):
        return Offer.objects.all().distinct()
    

class OffersDetailViewset(viewsets.ModelViewSet):
    queryset = OfferDetail.objects.all()  
    serializer_class = OfferDetailSerializer