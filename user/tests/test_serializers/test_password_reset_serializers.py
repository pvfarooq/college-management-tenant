from django.test import TestCase

from user.api.serializers import PasswordResetSerializer

from ..factory import UserFactory


class PasswordResetSerializerTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.data = {
            "email": self.user.email,
        }
        self.serializer = PasswordResetSerializer

    def test_password_reset_serializer(self):
        serializer = self.serializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data, self.data)

    def test_password_reset_serializer_invalid_email(self):
        self.data["email"] = "invalid_email"
        serializer = self.serializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["email"][0], "Enter a valid email address.")

    def test_password_reset_serializer_email_does_not_exist(self):
        self.data["email"] = "unknownuser@cms.in"
        serializer = self.serializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["email"][0], "Email does not exist.")
