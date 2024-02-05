from django.test import TestCase

from core.exceptions import DateOrderViolationError, DuplicateAlternateTimeTableEntry

from ..factory import AlternateTimeTableFactory


class AlternateTimeTableTestCase(TestCase):
    def setUp(self):
        self.alternate_timetable = AlternateTimeTableFactory()

    def test_str(self):
        self.assertEqual(
            str(self.alternate_timetable),
            f"Alternate for {self.alternate_timetable.default_timetable}",
        )

    def test_save(self):
        self.alternate_timetable.save()

    def test_start_date_greater_than_end_date(self):
        with self.assertRaises(DateOrderViolationError) as cm:
            AlternateTimeTableFactory(
                start_date=self.alternate_timetable.end_date,
                end_date=self.alternate_timetable.start_date,
            )
        self.assertEqual(
            str(cm.exception),
            f"Given date {self.alternate_timetable.end_date} is less than the reference date.",
        )

    def test_duplicate_alternate_timetable_entry(self):
        with self.assertRaises(DuplicateAlternateTimeTableEntry) as cm:
            AlternateTimeTableFactory(
                default_timetable=self.alternate_timetable.default_timetable,
                faculty=self.alternate_timetable.faculty,
                start_date=self.alternate_timetable.start_date,
                end_date=self.alternate_timetable.end_date,
            )
        self.assertEqual(
            str(cm.exception),
            "An alternate timetable already exists for the given date range.",
        )
