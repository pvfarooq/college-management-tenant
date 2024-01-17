from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..factory import UserFactory


class PasswordResetLinkViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse("password_reset")

    def test_password_reset_link(self):
        data = {"email": self.user.email}
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Password reset link sent to email.")
        self.assertIn("reset_link", response.data)

    def test_password_reset_link_invalid_email(self):
        data = {"email": "unknownuser@cms.in"}
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["email"][0], "Email does not exist.")
