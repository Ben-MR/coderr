from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user_auth_app.models import CustomUser
from profile_app.models import UserProfile

class UserProfilePermissionsTests(APITestCase):

    @classmethod
    def _unauth_statuses(cls):
        return {status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN}

    def setUp(self):
        self.user_a = CustomUser.objects.create_user(
            username="user_a",
            email="a@example.com",
            password="sicheresPassword123a",
            type="customer"
        )
        self.profile_a, _ = UserProfile.objects.get_or_create(user=self.user_a)
        
        self.user_b = CustomUser.objects.create_user(
            username="user_b",
            email="b@example.com",
            password="sicheresPassword123b",
            type="business"
        )
        self.profile_b, _ = UserProfile.objects.get_or_create(user=self.user_b)
        
        self.profile_b.location = "Hamburg"
        self.profile_b.tel = "222"
        self.profile_b.save()

        self.detail_url_a = reverse("profile-detail", kwargs={"pk": self.profile_a.pk})
        self.detail_url_b = reverse("profile-detail", kwargs={"pk": self.profile_b.pk})
        
        self.customer_list_url = reverse("profiles-customer-type-list")
        self.business_list_url = reverse("profiles-business-type-list")

    def tearDown(self):
        self.client.credentials()

    def test_authenticated_can_access_own_profile(self):
        self.client.force_authenticate(user=self.user_a)
        resp = self.client.get(self.detail_url_a)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_owner_can_update_own_profile(self):
        self.client.force_authenticate(user=self.user_a)
        payload = {
            "first_name": "AliceUpdated",
            "last_name": "AUpdated",
            "location": "Berlin Mitte",
            "tel": "999",
            "description": "Updated",
            "working_hours": "8-16",
            "email": "alice.updated@example.com",
        }
        resp = self.client.patch(self.detail_url_a, data=payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.profile_a.refresh_from_db()
        self.user_a.refresh_from_db()
        self.assertEqual(self.profile_a.location, "Berlin Mitte")
        self.assertEqual(self.user_a.first_name, "AliceUpdated")

    def test_non_owner_cannot_update_someone_elses_profile(self):
        self.client.force_authenticate(user=self.user_a)
        payload = {"location": "Hacked"}
        resp = self.client.patch(self.detail_url_b, data=payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_list_returns_only_customer_profiles(self):
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get(self.customer_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user"], self.user_a.id)

    def test_business_list_returns_only_business_profiles(self):
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get(self.business_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user"], self.user_b.id)