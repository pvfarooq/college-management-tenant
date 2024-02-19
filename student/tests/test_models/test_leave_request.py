from datetime import date

from django.test import TestCase
from freezegun import freeze_time

from core.exceptions import DateOrderViolationError

from ..factory import LeaveRequestFactory


@freeze_time("2024-01-01")
class LeaveRequestTestCase(TestCase):
    def setUp(self):
        self.leave_request = LeaveRequestFactory(
            from_date=date(2024, 1, 1), to_date=date(2024, 1, 6)
        )

    def test_str_representation(self):
        self.assertEqual(
            str(self.leave_request),
            f"{self.leave_request.student.name} - {self.leave_request.status}",
        )

    def test_total_days(self):
        self.assertEqual(self.leave_request.total_days, 6)

    def test_validate_dates_with_past_date_from_date(self):
        with self.assertRaises(DateOrderViolationError) as cm:
            LeaveRequestFactory(from_date="2020-01-01", to_date="2020-01-06")

        self.assertEqual(
            str(cm.exception),
            "You cannot request leave for past dates",
        )

    def test_validate_dates_with_invalid_date_order(self):
        with self.assertRaises(DateOrderViolationError) as cm:
            LeaveRequestFactory(from_date="2021-01-06", to_date="2021-01-01")

        self.assertEqual(
            str(cm.exception),
            "'from_date' cannot be greater than 'to_date'",
        )
