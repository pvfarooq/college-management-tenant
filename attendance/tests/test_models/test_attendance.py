from django.test import TestCase
from django.utils import timezone

from core.exceptions import AttendanceEditWindowClosed, DuplicateAttendanceEntry
from core.tests.factory import CollegeSettingsFactory

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

    def test_unique_attendance_validation(self):
        with self.assertRaises(DuplicateAttendanceEntry):
            AttendanceFactory(
                batch=self.attendance.batch,
                semester=self.attendance.semester,
                date=self.attendance.date,
                student=self.attendance.student,
                time_slot=self.attendance.time_slot,
            )

    def test_check_edit_window_closed(self):
        college_settings = CollegeSettingsFactory()
        attendance = AttendanceFactory()

        with self.assertRaises(AttendanceEditWindowClosed) as context:
            attendance.created_at -= timezone.timedelta(
                days=college_settings.max_attendance_change_window_days + 1
            )
            attendance.save()
        self.assertEqual(
            str(context.exception),
            "Attendance edit window has closed after the allowed days.Contact admin for further assistance.",
        )
