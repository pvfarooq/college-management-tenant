from django.test import TestCase

from core.exceptions import TimeOrderViolationError

from ..factory import SpecialTimeSlotFactory


class SpecialTimeSlotTest(TestCase):
    def test_str_representation(self):
        special_time_slot = SpecialTimeSlotFactory()
        self.assertEqual(
            str(special_time_slot),
            f"{special_time_slot.start_time} - {special_time_slot.end_time} - ({special_time_slot.day})",
        )

    def test_start_time_less_than_end_time(self):
        with self.assertRaises(TimeOrderViolationError) as cm:
            SpecialTimeSlotFactory(start_time="12:00", end_time="11:00")
        self.assertEqual(
            str(cm.exception),
            "Given time (12:00) is less than the reference time. (code: time_order_violation)",
        )

    def test_start_time_equal_to_end_time(self):
        with self.assertRaises(TimeOrderViolationError) as cm:
            SpecialTimeSlotFactory(start_time="12:00", end_time="12:00")
        self.assertEqual(
            str(cm.exception),
            "Given time (12:00) is less than the reference time. (code: time_order_violation)",
        )

    def test_start_time_greater_than_end_time(self):
        special_time_slot = SpecialTimeSlotFactory(start_time="12:00", end_time="13:00")
        self.assertEqual(special_time_slot.start_time, "12:00")
        self.assertEqual(special_time_slot.end_time, "13:00")
