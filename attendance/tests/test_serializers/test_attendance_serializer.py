from django.test import TestCase

from attendance.api.serializers import AttendanceSerializer

from ..factory import AttendanceFactory


class AttendanceSerializerTestCase(TestCase):
    def setUp(self):
        self.attendance = AttendanceFactory()
        self.serializer = AttendanceSerializer

    def test_attendance_serializer(self):
        serializer = self.serializer(self.attendance)
        self.assertEqual(
            serializer.data,
            {
                "id": str(self.attendance.id),
                "batch": self.attendance.batch,
                "semester": self.attendance.semester,
                "time_slot": self.attendance.time_slot.id,
                "faculty": self.attendance.faculty.id,
                "student": self.attendance.student.id,
                "date": str(self.attendance.date),
                "is_present": self.attendance.is_present,
            },
        )

    def test_attendance_serializer_with_no_data(self):
        serializer = self.serializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["batch"][0], "This field is required.")
        self.assertEqual(serializer.errors["semester"][0], "This field is required.")
        self.assertEqual(serializer.errors["time_slot"][0], "This field is required.")
        self.assertEqual(serializer.errors["student"][0], "This field is required.")
        self.assertEqual(serializer.errors["date"][0], "This field is required.")
