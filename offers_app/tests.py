from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Offer, OfferDetail

User = get_user_model()

class OfferAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testworker', 
            password='password123',
            type='business'
        )
        
        self.customer_user = User.objects.create_user(
            username='customeruser', 
            password='password123',
            type='customer'
        )
        
        self.other_user = User.objects.create_user(
            username='otheruser', 
            password='password123',
            type='business'
        )
        
        self.offer = Offer.objects.create(
            user=self.user,
            title="Web Design",
            description="I build websites"
        )
        
        OfferDetail.objects.create(
            offer=self.offer, title="Basic", revisions=1, 
            delivery_time_in_days=10, price=100.00, offer_type="basic", features={}
        )
        OfferDetail.objects.create(
            offer=self.offer, title="Premium", revisions=5, 
            delivery_time_in_days=2, price=500.00, offer_type="premium", features={}
        )

        self.list_url = reverse('offers-list')
        self.detail_url = reverse('offers-detail', kwargs={'pk': self.offer.pk})

    def _get_results_list(self, response):
        if isinstance(response.data, dict) and 'results' in response.data:
            return response.data['results']
        return response.data if isinstance(response.data, list) else [response.data]


    def test_list_contains_min_values(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        results = self._get_results_list(response)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(results) > 0)
        
        first_item = results[0]
        self.assertIn('min_price', first_item)
        self.assertIn('min_delivery_time', first_item)
        self.assertEqual(float(first_item['min_price']), 100.00)
        self.assertEqual(first_item['min_delivery_time'], 2)

    def test_create_offer_authenticated_as_business(self):
        """Erfolgreiches Erstellen als Business-User."""
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "New Offer",
            "description": "Description",
            "details": [
                {
                    "title": "Standard",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": "250.00",
                    "features": {},
                    "offer_type": "standard"
                }
            ]
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 2)

    def test_create_offer_as_customer_denied(self):
        """Prüft, ob ein Customer am Erstellen gehindert wird (403)."""
        self.client.force_authenticate(user=self.customer_user)
        data = {
            "title": "Illegal Offer",
            "description": "I am a customer and should not create offers",
            "details": []
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_owner_only(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "details": [{"offer_type": "basic", "price": "120.00"}]
        }
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        basic_detail = OfferDetail.objects.get(offer=self.offer, offer_type="basic")
        self.assertEqual(float(basic_detail.price), 120.00)

    def test_update_foreign_offer_denied(self):
        """Andere Business-User dürfen fremde Angebote nicht ändern."""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(self.detail_url, {"title": "Hacked"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_by_creator(self):
        self.client.force_authenticate(user=self.user)
        url = f"{self.list_url}?creator_id={self.user.id}"
        response = self.client.get(url)
        results = self._get_results_list(response)
        self.assertEqual(len(results), 1)

    def test_search_title(self):
        self.client.force_authenticate(user=self.user)
        url = f"{self.list_url}?search=Web"
        response = self.client.get(url)
        results = self._get_results_list(response)
        self.assertEqual(len(results), 1)