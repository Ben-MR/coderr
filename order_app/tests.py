from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from order_app.models import Order
from offers_app.models import Offer, OfferDetail

User = get_user_model()

class OrderAPITests(APITestCase):

    def setUp(self):
        self.customer = User.objects.create_user(
            username='buyer', password='password123', type='customer'
        )
        self.seller = User.objects.create_user(
            username='seller', password='password123', type='business'
        )
        self.other_business = User.objects.create_user(
            username='other_biz', password='password123', type='business'
        )

        self.offer = Offer.objects.create(
            user=self.seller, title="Test Offer", description="Test"
        )
        self.detail = OfferDetail.objects.create(
            offer=self.offer, title="Basic", price=100.00, offer_type="basic",
            revisions=1, delivery_time_in_days=5, features={}
        )

        self.list_url = reverse('orders-list')

    def test_create_order_success(self):
        self.client.force_authenticate(user=self.customer)
        data = {"offer_detail_id": self.detail.id}
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        # Check ob Business User automatisch gesetzt wurde
        self.assertEqual(Order.objects.first().business_user, self.seller)

    def test_prevent_duplicate_order(self):
        Order.objects.create(
            customer_user=self.customer, 
            business_user=self.seller, 
            offer_detail=self.detail
        )
        self.client.force_authenticate(user=self.customer)
        data = {"offer_detail_id": self.detail.id}
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_order_as_seller_success(self):
        order = Order.objects.create(
            customer_user=self.customer, 
            business_user=self.seller, 
            offer_detail=self.detail,
            status='pending'
        )
        url = reverse('orders-detail', kwargs={'pk': order.pk})
        
        self.client.force_authenticate(user=self.seller) 
        data = {"status": "in_progress"}
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, "in_progress")

    def test_patch_order_as_buyer_forbidden(self):
        order = Order.objects.create(
            customer_user=self.customer, 
            business_user=self.seller, 
            offer_detail=self.detail
        )
        url = reverse('orders-detail', kwargs={'pk': order.pk})
        
        self.client.force_authenticate(user=self.customer) 
        response = self.client.patch(url, {"status": "completed"})
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_foreign_order_forbidden(self):
        order = Order.objects.create(
            customer_user=self.customer, 
            business_user=self.seller, 
            offer_detail=self.detail
        )
        url = reverse('orders-detail', kwargs={'pk': order.pk})
        
        self.client.force_authenticate(user=self.other_business)
        response = self.client.patch(url, {"status": "completed"})
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)