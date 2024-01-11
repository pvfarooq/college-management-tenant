from django.test import TestCase

from ..factory import ExamTypeFactory


class ExamTypeTestCase(TestCase):
    def setUp(self):
        self.exam_type = ExamTypeFactory()

    def test_str_representation(self):
        self.assertEqual(str(self.exam_type), self.exam_type.name)

    def test_unique_name(self):
        with self.assertRaises(Exception) as cm:
            ExamTypeFactory(name=self.exam_type.name)

        self.assertEqual(
            str(cm.exception.message),
            "An exam type with the given name already exists.",
        )

    def test_unique_name_case_insensitive(self):
        with self.assertRaises(Exception) as cm:
            ExamTypeFactory(name=self.exam_type.name.lower())

        self.assertEqual(
            str(cm.exception.message),
            "An exam type with the given name already exists.",
        )
