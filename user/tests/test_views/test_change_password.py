from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.test import APITestCase

from ..factory import UserFactory


class ChangePasswordViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = PasswordResetTokenGenerator().make_token(self.user)
        self.url = reverse(
            "reset_password", kwargs={"uidb64": self.uidb64, "token": self.token}
        )

    def test_change_password(self):
        data = {"password": "newpassword", "confirm_password": "newpassword"}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Password changed successfully.", response.data["message"])

    def test_change_password_invalid_link(self):
        url = reverse(
            "reset_password", kwargs={"uidb64": "invalid", "token": "invalid"}
        )
        data = {"password": "newpassword"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid link.", response.data["message"])

    def test_change_password_invalid_token(self):
        url = reverse(
            "reset_password", kwargs={"uidb64": self.uidb64, "token": "invalid"}
        )
        data = {"password": "newpassword"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid or expired link.", response.data["message"])
