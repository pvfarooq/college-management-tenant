from django.test import TestCase

from core.exceptions import TimeOrderViolationError


class TimeOrderViolationErrorTestCase(TestCase):
    def setUp(self):
        self.input_time = "12:00"
        self.error_detail = "Some error detail message"
        self.error_code = "time_order_violation"

    def test_with_error_detail(self):
        with self.assertRaises(TimeOrderViolationError) as cm:
            raise TimeOrderViolationError(
                input_time=self.input_time, error_detail=self.error_detail
            )

        exception = cm.exception
        self.assertEqual(exception.input_time, self.input_time)
        self.assertEqual(exception.error_detail, self.error_detail)
        self.assertEqual(exception.error_code, self.error_code)

    def test_without_error_detail(self):
        with self.assertRaises(TimeOrderViolationError) as cm:
            raise TimeOrderViolationError(input_time=self.input_time)

        exception = cm.exception
        self.assertEqual(exception.input_time, self.input_time)
        self.assertIsNone(exception.error_detail)
        self.assertEqual(exception.error_code, self.error_code)
        self.assertEqual(
            str(exception),
            f"Given time {self.input_time} is less than the reference time. (code: {self.error_code})",
        )

    def test_without_input_time(self):
        with self.assertRaises(TypeError) as cm:
            raise TimeOrderViolationError()

        exception = cm.exception
        self.assertIn(
            "missing 1 required positional argument: 'input_time'", str(exception)
        )
