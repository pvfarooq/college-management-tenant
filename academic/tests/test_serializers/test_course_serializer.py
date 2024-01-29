from django.test import TestCase

from academic.api.serializers import CourseSerializer

from ..factory import CourseFactory


class CourseSerializerTest(TestCase):
    def setUp(self):
        self.course = CourseFactory(code="CSE 101")
        self.serializer = CourseSerializer

    def test_course_serializer(self):
        serializer = self.serializer(self.course)
        self.assertEqual(
            serializer.data,
            {
                "id": str(self.course.id),
                "title": self.course.title,
                "code": self.course.code,
                "duration": self.course.duration,
                "auto_promotion": self.course.auto_promotion,
                "intake": self.course.intake,
                "department": self.course.department.id,
            },
        )

    def test_course_serializer_with_no_data(self):
        serializer = self.serializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["title"][0], "This field is required.")
        self.assertEqual(serializer.errors["duration"][0], "This field is required.")

    def test_unique_course_code(self):
        CourseFactory(code="CSE 102")
        serializer = self.serializer(data={"code": "CSE 102"})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["code"][0], "course with this code already exists."
        )
