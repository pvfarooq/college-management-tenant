from django.test import TestCase

from attendance.api.serializers import TimeSlotSerializer

from ..factory import TimeSlotFactory


class TimeSlotSerializerTestCase(TestCase):
    def setUp(self):
        self.timeslot = TimeSlotFactory()
        self.serializer = TimeSlotSerializer

    def test_timeslot_serializer(self):
        serializer = self.serializer(self.timeslot)
        self.assertEqual(
            serializer.data,
            {
                "id": str(self.timeslot.id),
                "start_time": self.timeslot.start_time,
                "end_time": self.timeslot.end_time,
            },
        )

    def test_timeslot_serializer_with_no_data(self):
        serializer = self.serializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["start_time"][0], "This field is required.")
        self.assertEqual(serializer.errors["end_time"][0], "This field is required.")
