from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..factory import SuperUserFactory, UserFactory


class DeactivateUserViewTestCase(APITestCase):
    def setUp(self):
        self.active_user = UserFactory()
        self.url = reverse("deactivate_user", kwargs={"user_id": self.active_user.id})
        self.admin_user = SuperUserFactory()
        self.user = UserFactory()

    def test_deactivate_user(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "User account deactivated.")

    def test_deactivate_user_unauthenticated(self):
        response = self.client.patch(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deactivate_user_authenticated_non_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deactivate_user_invalid_id(self):
        self.client.force_authenticate(user=self.admin_user)
        self.url = reverse("deactivate_user", kwargs={"user_id": 100})
        response = self.client.patch(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Not found.")
