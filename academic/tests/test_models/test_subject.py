from django.db.utils import IntegrityError
from django.test import TestCase

from ..factory import SubjectFactory


class SubjectTestCase(TestCase):
    def setUp(self):
        self.subject = SubjectFactory(title="Subject 1", code="S1")

    def test_str_representation(self):
        self.assertEqual(str(self.subject), "Subject 1")

    def test_subject_title(self):
        self.assertEqual(self.subject.title, "Subject 1")

    def test_with_no_code(self):
        with self.assertRaises(IntegrityError):
            SubjectFactory(title="Subject 2", code=None)

    def test_unique_code(self):
        SubjectFactory(title="Subject 2", code="S2")
        with self.assertRaises(IntegrityError):
            SubjectFactory(title="Subject 3", code="S2")
