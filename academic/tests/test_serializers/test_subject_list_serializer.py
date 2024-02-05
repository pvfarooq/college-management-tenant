from django.test import TestCase

from academic.api.serializers import SubjectListSerializer

from ..factory import SubjectFactory


class SubjectListSerializerTestCase(TestCase):
    def setUp(self):
        self.subject = SubjectFactory(code="CSE101")
        self.serializer = SubjectListSerializer

    def test_subject_list_serializer(self):
        serializer = self.serializer(self.subject)
        self.assertEqual(
            serializer.data,
            {
                "id": str(self.subject.id),
                "title": self.subject.title,
                "code": self.subject.code,
                "course": {
                    "id": str(self.subject.course.id),
                    "title": self.subject.course.title,
                },
                "stream": {
                    "id": str(self.subject.stream.id),
                    "title": self.subject.stream.title,
                },
                "semester": self.subject.semester,
                "credit": self.subject.credit,
                "is_elective": self.subject.is_elective,
                "is_lab": self.subject.is_lab,
                "is_common": self.subject.is_common,
            },
        )
