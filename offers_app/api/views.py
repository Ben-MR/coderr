import django_filters
from rest_framework import viewsets, filters
from offers_app.api.permissions import IsOwnOffer, IsBusinessUser
from offers_app.api.serializer import OfferDetailSerializer, OfferSerializer, OfferReadSerializer, OfferSingleReadSerializer, OfferUpdateSerializer
from offers_app.models import Offer, OfferDetail
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny

class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination class to limit the number of offers returned per request.
    Allows clients to set custom page sizes up to a maximum of 1000 items.
    """
    page_size = 10
    page_size_query_param = 'page_size' 
    max_page_size = 1000

class OfferFilter(django_filters.FilterSet):
    """
    Custom filter set for the Offer model.
    Allows filtering by the creator's user ID, a minimum price threshold, 
    and a maximum delivery time limit across nested offer details.
    """
    creator_id = django_filters.NumberFilter(field_name='user__id')
    min_price = django_filters.NumberFilter(field_name='details__price', lookup_expr='gte') 
    max_delivery_time = django_filters.NumberFilter(field_name='details__delivery_time_in_days', lookup_expr='lte')

    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price', 'max_delivery_time']


class OffersViewSet(viewsets.ModelViewSet):
    """
    Main ViewSet for handling service offers.
    Provides full CRUD functionality with dynamic serializer switching based on the action,
    integrated search, filtering, and custom permission handling.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']


    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the current action.
        Uses specialized serializers for reading lists, retrieving details, 
        creating new instances, or updating existing ones.
        """
        if self.action in ['create', 'update']:
            return OfferSerializer
        if self.action == "retrieve":
            return OfferSingleReadSerializer
        if self.action == 'partial_update':
            return OfferUpdateSerializer
        
        return OfferReadSerializer

    def get_permissions(self):
        """
        Determines the permissions required for the current action.
        - Deleting and updating requires ownership.
        - Creating requires the 'Business' user type.
        - Other actions use default permission settings.
        """
        if self.action in ["destroy", "partial_update"]:
            return [IsAuthenticated(), IsOwnOffer()]
        if self.action in "create":
            return [IsAuthenticated(), IsBusinessUser()]
        if self.action in "list":
            return [AllowAny()]
        return super().get_permissions()
    
    def get_authenticators(self):
        """
        Disable authentication for the 'list' action.
        Since self.action is not yet set, we check the request method 
        and the URL structure.
        """
        if self.request and self.request.method == 'GET' and not self.kwargs.get('pk'):
            return []
        return super().get_authenticators()
        
    
    def get_queryset(self):
        """
        Returns the queryset for the view.
        Applies 'distinct()' to prevent duplicate results when filtering over 
        related offer detail tiers.
        """
        return Offer.objects.all().distinct()
    

class OffersDetailViewset(viewsets.ModelViewSet):
    """
    ViewSet for accessing specific pricing tiers (OfferDetails) directly.
    Provides standard model operations for detailed service configurations.
    """
    queryset = OfferDetail.objects.all()  
    serializer_class = OfferDetailSerializer
    