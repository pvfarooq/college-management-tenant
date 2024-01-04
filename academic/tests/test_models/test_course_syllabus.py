import os

from django.test import TestCase

from academic.tests.factory import CourseSyllabusFactory


class CourseSyllabusTestCase(TestCase):
    def setUp(self):
        self.course_syllabus = CourseSyllabusFactory()

    def tearDown(self):
        if self.course_syllabus.attachment:
            os.remove(self.course_syllabus.attachment.path)

    def test_str_representation(self):
        self.assertEqual(str(self.course_syllabus), self.course_syllabus.course.title)

    def test_course_syllabus_file_name(self):
        self.assertEqual(
            "course/syllabus/cse_syllabus_2020.pdf",
            self.course_syllabus.attachment.name,
        )

    def test_course_syllabus_without_attachment(self):
        course_syllabus = CourseSyllabusFactory(attachment=None)
        self.assertIsNone(course_syllabus.attachment._file)
