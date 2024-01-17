from django.test import TestCase

from user.api.serializers import ResetPasswordSerializer


class ResetPasswordSerializerTestCase(TestCase):
    def setUp(self):
        self.data = {
            "password": "password",
            "confirm_password": "password",
        }
        self.serializer = ResetPasswordSerializer

    def test_reset_password_serializer(self):
        serializer = self.serializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data, self.data)

    def test_reset_password_serializer_passwords_do_not_match(self):
        self.data["confirm_password"] = "password1"
        serializer = self.serializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["non_field_errors"][0], "Passwords do not match."
        )

    def test_reset_password_serializer_password_short(self):
        self.data["password"] = "passwor"
        self.data["confirm_password"] = "passwor"
        serializer = self.serializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["password"][0],
            "Ensure this field has at least 8 characters.",
        )
