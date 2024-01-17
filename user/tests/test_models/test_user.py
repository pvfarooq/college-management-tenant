from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from user.enums import UserRole

from ..factory import SuperUserFactory, UserFactory


class UserTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.superuser = SuperUserFactory()

    def test_user_creation(self):
        """Test user can be created"""

        self.assertEqual(self.user.__str__(), self.user.username)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_superuser_creation(self):
        """Test superuser can be created"""

        self.assertEqual(self.superuser.__str__(), self.superuser.username)
        self.assertTrue(self.superuser.is_active)
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)
        self.assertEqual(self.superuser.role, UserRole.ADMIN)

    def test_password_is_encrypted(self):
        """Test password is encrypted"""
        self.assertNotEqual(self.user.password, "defaultpassword")
        self.assertTrue(self.user.check_password("defaultpassword"))

    def test_student_role(self):
        """Test user role is student"""

        user = UserFactory(is_student=True)
        self.assertEqual(user.role, UserRole.STUDENT)

    def test_faculty_role(self):
        """Test user role is faculty"""

        user = UserFactory(is_faculty=True)
        self.assertEqual(user.role, UserRole.FACULTY)

    def test_generate_password_reset_link(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = PasswordResetTokenGenerator().make_token(self.user)
        reset_url = reverse("reset_password", kwargs={"uidb64": uidb64, "token": token})
        expected_url = f"http://localhost:8000{reset_url}"

        self.assertEqual(self.user.generate_password_reset_link(), expected_url)

    def test_validate_password_reset_token(self):
        token = PasswordResetTokenGenerator().make_token(self.user)

        self.assertTrue(self.user.validate_password_reset_token(token))

    def test_get_user_from_uidb64(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))

        self.assertEqual(self.user, self.user.get_user_from_uidb64(uidb64))

    def test_get_user_from_uidb64_invalid(self):
        self.assertIsNone(self.user.get_user_from_uidb64("invalid"))
