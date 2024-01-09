from django.test import TestCase

from ..factory import AttendanceFactory


class AttendanceTestcase(TestCase):
    def setUp(self):
        self.attendance = AttendanceFactory()

    def test_str_representation(self):
        self.assertEqual(
            str(self.attendance),
            f"{self.attendance.date} - {self.attendance.student} - {self.attendance.time_slot}",
        )

    def test_save(self):
        self.attendance.save()
