from django.test import TestCase

from academic.api.serializers import CourseListSerializer

from ..factory import CourseFactory


class CourseListSerializerTest(TestCase):
    def setUp(self):
        self.course = CourseFactory(code="CSE 101")
        self.serializer = CourseListSerializer

    def test_course_list_serializer(self):
        serializer = self.serializer(self.course)
        self.assertEqual(
            serializer.data,
            {
                "id": str(self.course.id),
                "department": {
                    "id": str(self.course.department.id),
                    "title": self.course.department.title,
                    "code": self.course.department.code,
                },
                "title": self.course.title,
                "code": self.course.code,
                "duration": self.course.duration,
                "auto_promotion": self.course.auto_promotion,
                "intake": self.course.intake,
            },
        )
