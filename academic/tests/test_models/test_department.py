from django.db.utils import IntegrityError
from django.test import TestCase

from ..factory import DepartmentFactory


class DepartmentTestCase(TestCase):
    def setUp(self):
        self.department = DepartmentFactory(title="Department 1", code="D1")

    def test_department_name(self):
        self.assertEqual(self.department.title, "Department 1")

    def test_department_code(self):
        self.assertEqual(self.department.code, "D1")

    def test_department_str(self):
        self.assertEqual(str(self.department), "Department 1")

    def test_with_no_code(self):
        department = DepartmentFactory(title="Department 2")
        self.assertEqual(department.code, None)

    def test_unique_code(self):
        DepartmentFactory(title="Department 2", code="C1")
        with self.assertRaises(IntegrityError):
            DepartmentFactory(title="Department 3", code="C1")
