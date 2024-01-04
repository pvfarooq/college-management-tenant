from django.test import TestCase

from ..factory import TutorFactory


class TutorTestCase(TestCase):
    def test_str_representation(self):
        tutor = TutorFactory()
        self.assertEqual(str(tutor), tutor.faculty.user.get_full_name())

    def test_with_stream(self):
        tutor = TutorFactory()
        self.assertIsNotNone(tutor.stream)

    def test_without_stream(self):
        tutor = TutorFactory(stream=None)
        self.assertIsNone(tutor.stream)
