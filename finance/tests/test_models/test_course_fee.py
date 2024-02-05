from datetime import date

from django.test import TestCase
from freezegun import freeze_time

from core.exceptions import DateOrderViolationError

from ..factory import CourseFeeFactory


class CourseFeeTestCase(TestCase):
    def test_str_representation(self):
        course_fee = CourseFeeFactory()
        self.assertEqual(
            str(course_fee), f"{course_fee.course} - Fee: {course_fee.fee}"
        )

    def test_valid_from_is_greater_than_valid_to(self):
        with self.assertRaises(DateOrderViolationError) as context:
            CourseFeeFactory(valid_from=date(2021, 1, 1), valid_to=date(2020, 1, 31))
            self.assertEqual(
                str(context.exception),
                "'valid_from' date cannot be greater than 'valid_to' date.",
            )

    def test_is_active_is_false_post_valid_to_date(self):
        course_fee = CourseFeeFactory(
            valid_from=date(2022, 1, 1), valid_to=date(2022, 12, 31)
        )
        self.assertFalse(course_fee.is_active)

    @freeze_time("2023-01-01")
    def test_is_active_is_true_on_same_valid_dates(self):
        course_fee = CourseFeeFactory(
            valid_from=date(2023, 1, 1),
            valid_to=date(2023, 1, 1),
        )
        self.assertTrue(course_fee.is_active)

    def test_fee_value_rounding(self):
        course_fee = CourseFeeFactory(fee=100.000)
        self.assertEqual(course_fee.fee, 100.00)
