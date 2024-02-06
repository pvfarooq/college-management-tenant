from django.test import TestCase

from attendance.api.serializers import TimeTableListSerializer

from ..factory import TimeTableFactory


class TimeTableListSerializerTestCase(TestCase):
    def setUp(self):
        self.timetable = TimeTableFactory()
        self.serializer = TimeTableListSerializer

    def test_timetable_list_serializer(self):
        serializer = self.serializer(self.timetable)
        self.assertEqual(
            serializer.data,
            {
                "id": str(self.timetable.id),
                "batch": self.timetable.batch,
                "semester": self.timetable.semester,
                "day": self.timetable.day,
                "time_slot": {
                    "id": str(self.timetable.time_slot.id),
                    "start_time": self.timetable.time_slot.start_time,
                    "end_time": self.timetable.time_slot.end_time,
                },
                "course": self.timetable.course.title,
                "stream": self.timetable.stream.title,
                "subject": self.timetable.subject.title,
                "faculty": self.timetable.faculty.user.get_full_name(),
            },
        )
