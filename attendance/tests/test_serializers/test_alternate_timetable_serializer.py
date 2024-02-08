from django.test import TestCase

from attendance.api.serializers import AlternateTimeTableSerializer

from ..factory import AlternateTimeTableFactory


class AlternateTimeTableSerializerTestCase(TestCase):
    def setUp(self):
        self.alternate_timetable = AlternateTimeTableFactory()
        self.serializer = AlternateTimeTableSerializer

    def test_alternate_timetable_serializer(self):
        serializer = self.serializer(self.alternate_timetable)
        self.assertEqual(
            serializer.data,
            {
                "id": str(self.alternate_timetable.id),
                "batch": self.alternate_timetable.batch,
                "semester": self.alternate_timetable.semester,
                "default_timetable": self.alternate_timetable.default_timetable.id,
                "faculty": self.alternate_timetable.faculty.id,
                "start_date": str(self.alternate_timetable.start_date),
                "end_date": str(self.alternate_timetable.end_date),
                "reason": self.alternate_timetable.reason,
            },
        )

    def test_with_no_data(self):
        serializer = self.serializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors,
            {
                "default_timetable": ["This field is required."],
                "faculty": ["This field is required."],
                "start_date": ["This field is required."],
                "end_date": ["This field is required."],
            },
        )
