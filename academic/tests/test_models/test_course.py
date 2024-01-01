from django.db.utils import IntegrityError
from django.test import TestCase

from ..factory import CourseFactory


class CourseTestCase(TestCase):
    def setUp(self):
        self.course = CourseFactory(title="Course 1", code="C1")

    def test_course_name(self):
        self.assertEqual(self.course.title, "Course 1")

    def test_course_code(self):
        self.assertEqual(self.course.code, "C1")

    def test_course_str(self):
        self.assertEqual(str(self.course), "Course 1")

    def test_with_no_code(self):
        course = CourseFactory(title="Course 2")
        self.assertEqual(course.code, None)

    def test_unique_code(self):
        CourseFactory(title="Course 2", code="C2")
        with self.assertRaises(IntegrityError):
            CourseFactory(title="Course 3", code="C2")
