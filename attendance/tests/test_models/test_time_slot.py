from django.test import TestCase

from core.exceptions import TimeOrderViolationError

from ..factory import TimeSlotFactory


class TimeSlotTest(TestCase):
    def test_str_representation(self):
        time_slot = TimeSlotFactory()
        self.assertEqual(
            str(time_slot), f"{time_slot.start_time} - {time_slot.end_time}"
        )

    def test_start_time_less_than_end_time(self):
        with self.assertRaises(TimeOrderViolationError) as cm:
            TimeSlotFactory(start_time="12:00", end_time="11:00")
        self.assertEqual(
            str(cm.exception),
            (
                "start time '12:00' must be less than the end time '11:00'"
                if not cm.exception.error_detail
                else cm.exception.error_detail
            ),
        )

    def test_start_time_equal_to_end_time(self):
        with self.assertRaises(TimeOrderViolationError) as cm:
            TimeSlotFactory(start_time="12:00", end_time="12:00")
        self.assertEqual(
            str(cm.exception),
            (
                "start time '12:00' must be less than the end time '12:00'"
                if not cm.exception.error_detail
                else cm.exception.error_detail
            ),
        )

    def test_start_time_greater_than_end_time(self):
        time_slot = TimeSlotFactory(start_time="12:00", end_time="13:00")
        self.assertEqual(time_slot.start_time, "12:00")
        self.assertEqual(time_slot.end_time, "13:00")
