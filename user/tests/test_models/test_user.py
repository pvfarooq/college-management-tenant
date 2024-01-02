from django.test import TestCase

from user.enums import UserRole

from ..factory import SuperUserFactory, UserFactory


class UserTestCase(TestCase):
    def test_user_creation(self):
        """Test user can be created"""

        user = UserFactory()
        self.assertEqual(user.__str__(), user.username)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_superuser_creation(self):
        """Test superuser can be created"""

        user = SuperUserFactory()
        self.assertEqual(user.__str__(), user.username)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.role, UserRole.ADMIN)

    def test_password_is_encrypted(self):
        """Test password is encrypted"""
        user = UserFactory()
        self.assertNotEqual(user.password, "defaultpassword")
        self.assertTrue(user.check_password("defaultpassword"))

    def test_student_role(self):
        """Test user role is student"""

        user = UserFactory(is_student=True)
        self.assertEqual(user.role, UserRole.STUDENT)

    def test_faculty_role(self):
        """Test user role is faculty"""

        user = UserFactory(is_faculty=True)
        self.assertEqual(user.role, UserRole.FACULTY)
