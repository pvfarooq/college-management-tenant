from django.db.utils import IntegrityError
from django.test import TestCase

from ..factory import StreamFactory


class StreamTestCase(TestCase):
    def setUp(self):
        self.stream = StreamFactory(title="Stream 1", code="S1")

    def test_stream_name(self):
        self.assertEqual(self.stream.title, "Stream 1")

    def test_stream_code(self):
        self.assertEqual(self.stream.code, "S1")

    def test_stream_str(self):
        self.assertEqual(str(self.stream), "Stream 1")

    def test_with_no_code(self):
        stream = StreamFactory(title="Stream 2")
        self.assertEqual(stream.code, None)

    def test_unique_code(self):
        StreamFactory(title="Stream 2", code="S2")
        with self.assertRaises(IntegrityError):
            StreamFactory(title="Stream 3", code="S2")
