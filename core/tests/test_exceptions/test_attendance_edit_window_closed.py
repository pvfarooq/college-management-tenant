from django.test import TestCase

from core.exceptions import AttendanceEditWindowClosed


class AttendanceEditWindowClosedTestCase(TestCase):
    def setUp(self):
        self.error_code = "attendance_edit_window_closed"

    def test_attendance_edit_window_closed(self):
        attendance_edit_window_closed = AttendanceEditWindowClosed()
        self.assertEqual(attendance_edit_window_closed.error_code, self.error_code)
        self.assertEqual(
            attendance_edit_window_closed.default_error_message(),
            "Attendance edit window has closed after the allowed days.Contact admin for further assistance.",
        )
