from datetime import date

from django.test import TestCase

from core.exceptions import DateOrderViolationError

from ..factory import LeaveRequestFactory


class LeaveRequestTestCase(TestCase):
    def setUp(self):
        self.leave_request = LeaveRequestFactory(
            from_date=date(2021, 1, 1), to_date=date(2021, 1, 6)
        )

    def test_str_representation(self):
        self.assertEqual(
            str(self.leave_request),
            f"{self.leave_request.student.name} - {self.leave_request.status}",
        )

    def test_total_days(self):
        self.assertEqual(self.leave_request.total_days, 6)

    def test_validate_dates(self):
        with self.assertRaises(DateOrderViolationError) as cm:
            LeaveRequestFactory(from_date="2021-01-06", to_date="2021-01-01")
        self.assertEqual(
            str(cm.exception),
            "'to_date' cannot be greater than 'from_date'",
        )
