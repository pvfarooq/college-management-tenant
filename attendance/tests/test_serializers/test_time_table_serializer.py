from django.test import TestCase

from attendance.api.serializers import TimeTableSerializer

from ..factory import TimeTableFactory


class TimeSlotSerializerTestCase(TestCase):
    def setUp(self):
        self.time_table = TimeTableFactory()
        self.serializer = TimeTableSerializer

    def test_time_table_serializer(self):
        serializer = self.serializer(self.time_table)
        self.assertEqual(
            serializer.data,
            {
                "id": str(self.time_table.id),
                "batch": self.time_table.batch,
                "semester": self.time_table.semester,
                "day": self.time_table.day,
                "time_slot": self.time_table.time_slot.id,
                "course": self.time_table.course.id,
                "stream": self.time_table.stream.id,
                "subject": self.time_table.subject.id,
                "faculty": self.time_table.faculty.id,
            },
        )

    def test_time_table_serializer_with_no_data(self):
        serializer = self.serializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["batch"][0], "This field is required.")
        self.assertEqual(serializer.errors["semester"][0], "This field is required.")
        self.assertEqual(serializer.errors["day"][0], "This field is required.")
        self.assertEqual(serializer.errors["time_slot"][0], "This field is required.")
        self.assertEqual(serializer.errors["course"][0], "This field is required.")
        self.assertEqual(serializer.errors["subject"][0], "This field is required.")
        self.assertEqual(serializer.errors["faculty"][0], "This field is required.")
