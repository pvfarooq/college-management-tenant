from django.db.utils import IntegrityError
from django.test import TestCase

from ..factory import FacultyRoleFactory


class FacultyRoleTestCase(TestCase):
    def test_str_representation(self):
        faculty_role = FacultyRoleFactory()
        self.assertEqual(str(faculty_role), faculty_role.title)

    def test_create_with_title_only(self):
        faculty_role = FacultyRoleFactory(description=None)
        self.assertIsNotNone(faculty_role.pk)
        self.assertIsNotNone(faculty_role.title)
        self.assertIsNone(faculty_role.description)

    def test_unique_title(self):
        FacultyRoleFactory(title="HOD")
        with self.assertRaises(IntegrityError):
            FacultyRoleFactory(title="HOD")
