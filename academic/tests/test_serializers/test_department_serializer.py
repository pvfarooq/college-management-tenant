from django.test import TestCase

from academic.api.serializers import DepartmentSerializer

from ..factory import DepartmentFactory


class DepartmentSerializerTest(TestCase):
    def setUp(self):
        self.department = DepartmentFactory(code="CS")
        self.serializer = DepartmentSerializer

    def test_department_serializer(self):
        serializer = self.serializer(self.department)
        self.assertEqual(
            serializer.data,
            {
                "id": str(self.department.id),
                "title": self.department.title,
                "code": self.department.code,
            },
        )

    def test_department_serializer_with_no_data(self):
        serializer = self.serializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["title"][0], "This field is required.")

    def test_unique_department_code(self):
        serializer = self.serializer(
            data={"title": "Computer Science ABC", "code": "CS"}
        )
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["code"][0], "department with this code already exists."
        )
