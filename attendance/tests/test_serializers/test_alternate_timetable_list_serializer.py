from django.test import TestCase

from attendance.api.serializers import AlternateTimeTableListSerializer

from ..factory import AlternateTimeTableFactory


class AlternateTimeTableListSerializerTestCase(TestCase):
    def setUp(self):
        self.alt_timetable = AlternateTimeTableFactory()
        self.serializer = AlternateTimeTableListSerializer

    def test_alternate_timetable_list_serializer(self):
        serializer = self.serializer(self.alt_timetable)
        serialized_data = serializer.data
        serialized_data["default_timetable"] = dict(
            serialized_data["default_timetable"]
        )
        serialized_data["default_timetable"]["time_slot"] = dict(
            serialized_data["default_timetable"]["time_slot"]
        )

        expected_data = {
            "id": str(self.alt_timetable.id),
            "faculty": self.alt_timetable.faculty.user.get_full_name(),
            "default_timetable": {
                "id": str(self.alt_timetable.default_timetable.id),
                "time_slot": {
                    "id": str(self.alt_timetable.default_timetable.time_slot.id),
                    "start_time": str(
                        self.alt_timetable.default_timetable.time_slot.start_time
                    ),
                    "end_time": str(
                        self.alt_timetable.default_timetable.time_slot.end_time
                    ),
                },
                "course": self.alt_timetable.default_timetable.course.title,
                "stream": self.alt_timetable.default_timetable.stream.title,
                "subject": self.alt_timetable.default_timetable.subject.title,
                "faculty": self.alt_timetable.default_timetable.faculty.user.get_full_name(),
                "batch": self.alt_timetable.default_timetable.batch,
                "semester": self.alt_timetable.default_timetable.semester,
                "day": self.alt_timetable.default_timetable.day,
            },
            "batch": self.alt_timetable.batch,
            "semester": self.alt_timetable.semester,
            "start_date": str(self.alt_timetable.start_date),
            "end_date": str(self.alt_timetable.end_date),
            "reason": self.alt_timetable.reason,
        }

        self.assertEqual(
            serialized_data,
            expected_data,
        )
