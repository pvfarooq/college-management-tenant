from django.test import TestCase

from academic.api.serializers import SubjectSerializer

from ..factory import SubjectFactory


class SubjectSerializerTestCase(TestCase):
    def setUp(self):
        self.subject = SubjectFactory(code="CSE101")
        self.serializer = SubjectSerializer

    def test_subject_serializer(self):
        serializer = self.serializer(self.subject)
        self.assertEqual(
            serializer.data,
            {
                "id": str(self.subject.id),
                "title": self.subject.title,
                "code": self.subject.code,
                "course": self.subject.course.id,
                "stream": self.subject.stream.id,
                "semester": self.subject.semester,
                "credit": self.subject.credit,
                "is_elective": self.subject.is_elective,
                "is_lab": self.subject.is_lab,
                "is_active": self.subject.is_active,
            },
        )

    def test_subject_serializer_required_fields(self):
        serializer = self.serializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            set(serializer.errors.keys()),
            {
                "title",
                "code",
                "course",
                "semester",
            },
        )

    def test_subject_serializer_unique_code(self):
        subject = SubjectFactory()
        serializer = self.serializer(
            data={
                "title": subject.title,
                "code": subject.code,
                "course": subject.course.id,
                "semester": subject.semester,
            }
        )
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            set(serializer.errors.keys()),
            {
                "code",
            },
        )
        self.assertEqual(
            serializer.errors["code"],
            ["subject with this code already exists."],
        )

    def test_create_subject_without_stream(self):
        subject = SubjectFactory()
        serializer = self.serializer(
            data={
                "title": subject.title,
                "code": "CSE110",
                "course": subject.course.id,
                "semester": subject.semester,
            }
        )
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})
