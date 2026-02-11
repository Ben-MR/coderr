from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from offers_app.models import OfferDetail
from order_app.api.permissions import IsAdmin, IsBusinessUser, IsCustomer
from order_app.api.serializer import OderSerializer, OrderUpdateSerializer
from order_app.models import Order
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()   
    serializer_class = OderSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    
    def perform_create(self, serializer):
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
        if self.action == 'partial_update':
            return OrderUpdateSerializer
        
        return OderSerializer
        
    def get_permissions(self):
        if self.action == "partial_update":
            return [IsAuthenticated(), IsBusinessUser()]
        if self.action in "destroy":
            return [IsAuthenticated(), IsAdmin()]
        return super().get_permissions()

class OrderCountViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        order_count = Order.objects.filter(business_user_id=pk).count()
        return Response({'order_count': order_count}, status=status.HTTP_200_OK)
    
class OrderCompletedCountViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
  
    def retrieve(self, request, pk=None):
        order_completed_count = Order.objects.filter(business_user_id=pk, status='completed').count()
        return Response({'completed_order_count': order_completed_count}, status=status.HTTP_200_OK)
    