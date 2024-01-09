from datetime import date

from django.test import TestCase

from core.exceptions import DateOrderViolationError


class DateOrderViolationTestCase(TestCase):
    def setUp(self):
        self.input_date = date(2022, 1, 1)
        self.error_detail = "Some error detail message"
        self.error_code = "date_order_violation"

    def test_with_error_detail(self):
        # checks if the exception is raised with the given error detail and it matches with the expected error detail
        with self.assertRaises(DateOrderViolationError) as cm:
            raise DateOrderViolationError(
                input_date=self.input_date, error_detail=self.error_detail
            )

        exception = cm.exception
        self.assertEqual(exception.input_date, self.input_date)
        self.assertEqual(exception.error_detail, self.error_detail)
        self.assertEqual(exception.error_code, self.error_code)

    def test_without_error_detail(self):
        # checks if the exception is raised without the given error detail and it matches with the expected error detail
        with self.assertRaises(DateOrderViolationError) as cm:
            raise DateOrderViolationError(input_date=self.input_date)

        exception = cm.exception
        self.assertEqual(exception.input_date, self.input_date)
        self.assertIsNone(exception.error_detail)
        self.assertEqual(exception.error_code, self.error_code)
        self.assertEqual(
            str(exception),
            f"Given date {self.input_date} is less than the reference date. (code: {self.error_code})",
        )

    def test_without_input_date(self):
        # checks if the exception is not raised without the given input date
        with self.assertRaises(TypeError) as cm:
            raise DateOrderViolationError()

        exception = cm.exception
        self.assertIn(
            "missing 1 required positional argument: 'input_date'", str(exception)
        )
