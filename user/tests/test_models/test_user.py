from django.test import TestCase
from ..factory import UserFactory, SuperUserFactory


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

    def test_password_is_encrypted(self):
        """Test password is encrypted"""
        user = UserFactory()
        self.assertNotEqual(user.password, "defaultpassword")
        self.assertTrue(user.check_password("defaultpassword"))

    

    