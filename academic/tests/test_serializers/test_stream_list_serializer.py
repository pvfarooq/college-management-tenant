from django.test import TestCase

from academic.api.serializers import StreamListSerializer

from ..factory import StreamFactory


class StreamListSerializerTestCase(TestCase):
    def setUp(self):
        self.stream = StreamFactory(code="CSE 101 B")
        self.serializer = StreamListSerializer

    def test_stream_list_serializer(self):
        serializer = self.serializer(self.stream)
        self.assertEqual(
            serializer.data,
            {
                "id": str(self.stream.id),
                "title": self.stream.title,
                "code": self.stream.code,
                "course": {
                    "id": str(self.stream.course.id),
                    "title": self.stream.course.title,
                },
            },
        )
