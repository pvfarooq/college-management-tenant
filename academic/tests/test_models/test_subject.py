from django.db.utils import IntegrityError
from django.test import TestCase

from core.exceptions import SubjectConstraintError

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

    def test_with_no_course(self):
        with self.assertRaises(SubjectConstraintError) as context:
            SubjectFactory(title="Engineering Mechanics", code="EM-102", course=None)
        self.assertIn(
            "Either 'course' should be set or 'is_common' should be set",
            str(context.exception),
        )

    def test_with_no_stream(self):
        subject = SubjectFactory(
            title="Engineering Mechanics", code="EM-102", stream=None
        )
        self.assertIsNone(subject.stream)
        self.assertEqual(subject.code, "EM-102")
        self.assertEqual(subject.title, "Engineering Mechanics")

    def test_with_no_semester(self):
        with self.assertRaises(IntegrityError) as context:
            SubjectFactory(title="Engineering Mechanics", code="EM-102", semester=None)
        self.assertIn("null value in column", str(context.exception))

    def test_with_no_course_and_not_common(self):
        with self.assertRaises(SubjectConstraintError) as context:
            SubjectFactory(
                title="Engineering Mechanics",
                code="EM-102",
                course=None,
                is_common=False,
            )
        self.assertIn(
            "Either 'course' should be set or 'is_common' should be set",
            str(context.exception),
        )

    def test_with_course_and_common(self):
        with self.assertRaises(SubjectConstraintError) as context:
            SubjectFactory(
                title="Engineering Mechanics",
                code="EM-102",
                course=self.subject.course,
                is_common=True,
            )
        self.assertIn(
            "Either 'course' should be set or 'is_common' should be set, not both.",
            str(context.exception),
        )
