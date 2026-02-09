from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from offers_app.models import OfferDetail
from order_app.api.permissions import IsCustomer
from order_app.api.serializer import OderSerializer
from order_app.models import Order

class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()   
    serializer_class = OderSerializer
    permission_classes = [IsAuthenticated(), IsCustomer()]
    
    def perform_create(self, serializer):
        od_id = self.request.data.get('offer_detail_id')
        offer_detail_obj = OfferDetail.objects.get(id=od_id)
        seller = offer_detail_obj.offer.user

        serializer.save(
            customer_user=self.request.user,
            business_user=seller,
            offer_detail=offer_detail_obj
    )