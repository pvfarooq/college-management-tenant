from django.test import TestCase

from attendance.api.serializers import AttendanceListSerializer

from ..factory import AttendanceFactory


class AttendanceListSerializerTestCase(TestCase):
    def setUp(self):
        self.attendance = AttendanceFactory()
        self.serializer = AttendanceListSerializer

    def test_attendance_list_serializer(self):
        serializer = self.serializer(self.attendance)
        self.assertEqual(
            serializer.data,
            {
                "id": str(self.attendance.id),
                "batch": self.attendance.batch,
                "semester": self.attendance.semester,
                "date": str(self.attendance.date),
                "time_slot": {
                    "id": str(self.attendance.time_slot.id),
                    "start_time": self.attendance.time_slot.start_time,
                    "end_time": self.attendance.time_slot.end_time,
                },
                "faculty": str(self.attendance.faculty),
                "student": self.attendance.student.name,
                "is_present": self.attendance.is_present,
            },
        )
