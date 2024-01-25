from django.test import TestCase

from core.exceptions import TimeOrderViolationError


class TimeOrderViolationErrorTestCase(TestCase):
    def setUp(self):
        self.start_time = "12:00"
        self.end_time = "13:00"
        self.error_detail = "Some error detail message"
        self.error_code = "time_order_violation"

    def test_with_error_detail(self):
        with self.assertRaises(TimeOrderViolationError) as cm:
            raise TimeOrderViolationError(
                start_time=self.start_time,
                end_time=self.end_time,
                error_detail=self.error_detail,
            )

        exception = cm.exception
        self.assertEqual(exception.start_time, self.start_time)
        self.assertEqual(exception.end_time, self.end_time)
        self.assertEqual(exception.error_detail, self.error_detail)
        self.assertEqual(exception.error_code, self.error_code)

    def test_without_error_detail(self):
        with self.assertRaises(TimeOrderViolationError) as cm:
            raise TimeOrderViolationError(
                start_time=self.start_time, end_time=self.end_time
            )

        exception = cm.exception
        self.assertEqual(exception.start_time, self.start_time)
        self.assertEqual(exception.end_time, self.end_time)
        self.assertIsNone(exception.error_detail)
        self.assertEqual(exception.error_code, self.error_code)
        self.assertEqual(
            str(exception),
            f"start time '{self.start_time}' must be less than the end time"
            f" '{self.end_time}' (code: {self.error_code})",
        )

    def test_without_start_time(self):
        with self.assertRaises(TypeError) as cm:
            raise TimeOrderViolationError(end_time=self.end_time)

        exception = cm.exception
        self.assertIn(
            "missing 1 required positional argument: 'start_time'", str(exception)
        )

    def test_without_end_time(self):
        with self.assertRaises(TypeError) as cm:
            raise TimeOrderViolationError(start_time=self.start_time)

        exception = cm.exception
        self.assertIn(
            "missing 1 required positional argument: 'end_time'", str(exception)
        )
