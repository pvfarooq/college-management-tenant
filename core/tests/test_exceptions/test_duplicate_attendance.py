from django.test import TestCase

from core.exceptions import DuplicateAttendanceEntry


class DuplicateAttendanceEntryTestCase(TestCase):
    def setUp(self):
        self.error_detail = "Some error detail message"
        self.error_code = "duplicate_attendance_entry"

    def test_with_error_detail(self):
        with self.assertRaises(DuplicateAttendanceEntry) as cm:
            raise DuplicateAttendanceEntry(error_detail=self.error_detail)

        exception = cm.exception
        self.assertEqual(exception.error_detail, self.error_detail)
        self.assertEqual(exception.error_code, self.error_code)

    def test_without_error_detail(self):
        with self.assertRaises(DuplicateAttendanceEntry) as cm:
            raise DuplicateAttendanceEntry()

        exception = cm.exception
        self.assertIsNone(exception.error_detail)
        self.assertEqual(exception.error_code, self.error_code)
        self.assertEqual(
            str(exception),
            f"An attendance already exists for the given date, time slot and student. (code: {self.error_code})",
        )
