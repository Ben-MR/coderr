from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from reviews_app.models import Reviews

User = get_user_model()

class ReviewAPITests(APITestCase):

    def setUp(self):
        # User anlegen
        self.customer = User.objects.create_user(
            username='buyer', password='password123', type='customer'
        )
        self.seller = User.objects.create_user(
            username='seller', password='password123', type='business'
        )
        self.other_customer = User.objects.create_user(
            username='other', password='password123', type='customer'
        )

        # URLs
        self.list_url = reverse('reviews-list')

    def test_create_review_success(self):
        """Ein Kunde kann einen Business-User bewerten."""
        self.client.force_authenticate(user=self.customer)
        data = {
            "business_user": self.seller.id,
            "rating": 5,
            "description": "Top Service!"
        }
        response = self.client.post(self.list_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reviews.objects.count(), 1)
        self.assertEqual(Reviews.objects.first().reviewer, self.customer)

    def test_prevent_duplicate_review(self):
        """Verhindert, dass ein Kunde denselben Business-User zweimal bewertet."""
        Reviews.objects.create(
            reviewer=self.customer,
            business_user=self.seller,
            rating=4,
            description="Erster Versuch"
        )
        self.client.force_authenticate(user=self.customer)
        data = {
            "business_user": self.seller.id,
            "rating": 1,
            "description": "Zweiter Versuch"
        }
        response = self.client.post(self.list_url, data)
        
        # Hier greift dein manueller Check in perform_create (400 Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_review_only_by_owner(self):
        """Nur der Ersteller (Reviewer) darf seine Bewertung bearbeiten."""
        review = Reviews.objects.create(
            reviewer=self.customer,
            business_user=self.seller,
            rating=5,
            description="Original"
        )
        url = reverse('reviews-detail', kwargs={'pk': review.pk})
        
        # Test 1: Fremder Kunde versucht es -> Forbidden
        self.client.force_authenticate(user=self.other_customer)
        response = self.client.patch(url, {"rating": 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test 2: Der echte Besitzer versucht es -> OK
        self.client.force_authenticate(user=self.customer)
        response = self.client.patch(url, {"rating": 4})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_business_user_cannot_create_review(self):
        """Ein Business-User darf keine Reviews erstellen (IsCustomer Permission)."""
        self.client.force_authenticate(user=self.seller)
        data = {"business_user": self.seller.id, "rating": 5, "description": "Eigenlob"}
        response = self.client.post(self.list_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_reviews_by_business_user(self):
        """Testet dein ReviewFilter (business_user_id)."""
        Reviews.objects.create(reviewer=self.customer, business_user=self.seller, rating=5, description="A")
        
        self.client.force_authenticate(user=self.customer)
        # Filter anwenden: ?business_user_id=...
        response = self.client.get(self.list_url, {'business_user_id': self.seller.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Sicherstellen, dass nur das eine Review zurückkommt
        self.assertEqual(len(response.data), 1)