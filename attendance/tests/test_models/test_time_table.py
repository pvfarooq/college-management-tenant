from django.test import TestCase

from core.exceptions import DuplicateTimeTableEntry

from ..factory import TimeTableFactory


class TimeTableTestCase(TestCase):
    def setUp(self):
        self.timetable = TimeTableFactory()

    def test_str(self):
        self.assertEqual(
            str(self.timetable),
            f"{self.timetable.day} - {self.timetable.time_slot} - {self.timetable.subject}",
        )

    def test_save_valid_time_table(self):
        self.timetable.save()

    def test_duplicate_timetable_entry(self):
        with self.assertRaises(DuplicateTimeTableEntry) as cm:
            TimeTableFactory(
                batch=self.timetable.batch,
                semester=self.timetable.semester,
                day=self.timetable.day,
                time_slot=self.timetable.time_slot,
            )
        self.assertEqual(
            str(cm.exception),
            "A timetable already exists for the given day and time slot. (code: duplicate_timetable_entry)",
        )
