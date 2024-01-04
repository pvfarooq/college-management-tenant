from django.db.utils import IntegrityError
from django.test import TestCase

from ..factory import FacultyFactory, FacultyRoleFactory


class FacultyTestCase(TestCase):
    def test_str_representation(self):
        faculty = FacultyFactory()
        self.assertEqual(str(faculty), faculty.user.get_full_name())

    def test_faculty_without_roles(self):
        faculty = FacultyFactory(roles=[])
        self.assertEqual(faculty.roles.count(), 0)

    def test_faculty_with_multiple_roles(self):
        faculty = FacultyFactory(
            roles=[FacultyRoleFactory(), FacultyRoleFactory(), FacultyRoleFactory()]
        )
        self.assertEqual(faculty.roles.count(), 3)

    def test_uniqe_faculty_code(self):
        FacultyFactory(faculty_code="FAC_001")
        with self.assertRaises(IntegrityError):
            FacultyFactory(faculty_code="FAC_001")
