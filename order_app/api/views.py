from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from offers_app.models import OfferDetail
from order_app.api.permissions import IsAdmin, IsBusinessUser, IsCustomer
from order_app.api.serializer import OderSerializer, OrderUpdateSerializer
from order_app.models import Order
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Q

class OrdersViewSet(viewsets.ModelViewSet):
    """
    Main ViewSet for managing orders.
    
    Handles the creation of orders by customers and status updates by business users.
    Includes logic to prevent duplicate orders for the same offer detail by the same user.
    """
    queryset = Order.objects.all()   
    serializer_class = OderSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    
    def perform_create(self, serializer):
        """
        Creates a new order and assigns the customer and business user.
        
        Extracts the offer detail from the request data, identifies the seller,
        and checks if an active order for this specific package already exists 
        to prevent duplicates.
        """
        od_id = self.request.data.get('offer_detail_id')
        offer_detail_obj = OfferDetail.objects.get(id=od_id)
        seller = offer_detail_obj.offer.user

        if Order.objects.filter(customer_user=self.request.user, offer_detail=offer_detail_obj).exists():        
            raise ValidationError("Du hast dieses Paket bereits bestellt.")

        serializer.save(
            customer_user=self.request.user,
            business_user=seller,
            offer_detail=offer_detail_obj 
    )
        
    def get_serializer_class(self):
        """
        Returns specialized serializers depending on the action.
        Uses the UpdateSerializer for partial updates to handle status changes.
        """
        if self.action == 'partial_update':
            return OrderUpdateSerializer        
        return OderSerializer
    
    def get_queryset(self):
        """
        Returns the queryset of orders filtered by the current user's involvement.
        The Q objects are used to perform an OR filter between customer and business user.
        """
        user = self.request.user
        
        if user.is_superuser:
            return Order.objects.all()
            
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        ).distinct()
        
    def get_permissions(self):
        """
        Assigns permissions based on the action:
        - partial_update: Only the associated business user.
        - destroy: Only administrative accounts.
        - list/create: Authenticated customers.
        """
        if self.action == "partial_update":
            return [IsAuthenticated(), IsBusinessUser()]
        if self.action in "destroy":
            return [IsAuthenticated(), IsAdmin()]
        return super().get_permissions()

class OrderCountViewSet(viewsets.ViewSet):
    """
    A simple ViewSet to retrieve the total number of orders received by a specific business user.
    """
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        """
        Returns the count of all orders assigned to the business user identified by pk.
        """
        order_count = Order.objects.filter(business_user_id=pk).count()
        return Response({'order_count': order_count}, status=status.HTTP_200_OK)
    
class OrderCompletedCountViewSet(viewsets.ViewSet):
    """
    A ViewSet to retrieve the count of successfully finished orders for a specific business user.
    """
    permission_classes = [IsAuthenticated]
  
    def retrieve(self, request, pk=None):
        """
        Returns the count of orders with the status 'completed' for the business user identified by pk.
        """
        order_completed_count = Order.objects.filter(business_user_id=pk, status='completed').count()
        return Response({'completed_order_count': order_completed_count}, status=status.HTTP_200_OK)