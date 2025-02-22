from django.test import TestCase

from core.exceptions import DuplicateAlternateTimeTableEntry, DuplicateTimeTableEntry


class DuplicateTimeTableEntryTestCase(TestCase):
    def setUp(self):
        self.error_detail = "Some error detail message"
        self.error_code = "duplicate_timetable_entry"

    def test_with_error_detail(self):
        with self.assertRaises(DuplicateTimeTableEntry) as cm:
            raise DuplicateTimeTableEntry(error_detail=self.error_detail)

        exception = cm.exception
        self.assertEqual(exception.error_detail, self.error_detail)
        self.assertEqual(exception.error_code, self.error_code)

    def test_without_error_detail(self):
        with self.assertRaises(DuplicateTimeTableEntry) as cm:
            raise DuplicateTimeTableEntry()

        exception = cm.exception
        self.assertIsNone(exception.error_detail)
        self.assertEqual(exception.error_code, self.error_code)
        self.assertEqual(
            str(exception),
            "A timetable already exists for the given day and time slot.",
        )


class DuplicateAlternateTimeTableEntryTestCase(TestCase):
    def setUp(self):
        self.error_detail = "Some error detail message"
        self.error_code = "duplicate_alternate_timetable_entry"

    def test_with_error_detail(self):
        with self.assertRaises(DuplicateAlternateTimeTableEntry) as cm:
            raise DuplicateAlternateTimeTableEntry(error_detail=self.error_detail)

        exception = cm.exception
        self.assertEqual(exception.error_detail, self.error_detail)
        self.assertEqual(exception.error_code, self.error_code)

    def test_without_error_detail(self):
        with self.assertRaises(DuplicateAlternateTimeTableEntry) as cm:
            raise DuplicateAlternateTimeTableEntry()

        exception = cm.exception
        self.assertIsNone(exception.error_detail)
        self.assertEqual(exception.error_code, self.error_code)
        self.assertEqual(
            str(exception),
            "An alternate timetable already exists for the given date range.",
        )
