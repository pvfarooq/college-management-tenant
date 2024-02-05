from django.test import TestCase

from academic.api.serializers import CourseShortInfoSerializer

from ..factory import CourseFactory


class CourseShortInfoSerializerTest(TestCase):
    def setUp(self):
        self.course = CourseFactory(code="CSE 101")
        self.serializer = CourseShortInfoSerializer

    def test_serializer(self):
        serializer = self.serializer(self.course)
        self.assertEqual(
            serializer.data,
            {
                "id": str(self.course.id),
                "title": self.course.title,
            },
        )
