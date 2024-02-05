from django.test import TestCase

from academic.api.serializers import StreamShortInfoSerializer

from ..factory import StreamFactory


class StreamShortInfoSerializerTestCase(TestCase):
    def setUp(self):
        self.serializer = StreamShortInfoSerializer
        self.stream = StreamFactory(code="CS101-B")

    def test_serializer(self):
        serializer = self.serializer(self.stream)
        self.assertEqual(
            serializer.data,
            {
                "id": str(self.stream.id),
                "title": self.stream.title,
            },
        )
