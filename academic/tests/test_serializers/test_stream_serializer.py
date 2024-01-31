from django.test import TestCase

from academic.api.serializers import StreamSerializer

from ..factory import StreamFactory


class StreamSerializerTestCase(TestCase):
    def setUp(self):
        self.serializer = StreamSerializer
        self.stream = StreamFactory(code="CS101-B")

    def test_stream_serializer(self):
        serializer = self.serializer(self.stream)
        self.assertEqual(
            serializer.data,
            {
                "id": str(self.stream.id),
                "title": self.stream.title,
                "code": self.stream.code,
                "course": self.stream.course.id,
            },
        )

    def test_stream_serializer_with_no_data(self):
        serializer = self.serializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["title"][0], "This field is required.")
        self.assertEqual(serializer.errors["course"][0], "This field is required.")

    def test_unique_stream_code(self):
        data = {
            "title": "Computer Science",
            "course": self.stream.course.id,
            "code": self.stream.code,
        }
        serializer = self.serializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["code"][0], "stream with this code already exists."
        )
