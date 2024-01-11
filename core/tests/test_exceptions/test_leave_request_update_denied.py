from django.test import TestCase

from core.exceptions import LeaveRequestUpdateDeniedError


class LeaveRequestUpdateDeniedErrorTestCase(TestCase):
    def setUp(self):
        self.error_detail = "Some error detail message"
        self.error_code = "leave_request_update_denied"

    def test_with_error_detail(self):
        with self.assertRaises(LeaveRequestUpdateDeniedError) as cm:
            raise LeaveRequestUpdateDeniedError(error_detail=self.error_detail)

        exception = cm.exception
        self.assertEqual(exception.error_detail, self.error_detail)
        self.assertEqual(exception.error_code, self.error_code)

    def test_without_error_detail(self):
        with self.assertRaises(LeaveRequestUpdateDeniedError) as cm:
            raise LeaveRequestUpdateDeniedError()

        exception = cm.exception
        self.assertIsNone(exception.error_detail)
        self.assertEqual(exception.error_code, self.error_code)
        self.assertEqual(
            str(exception),
            f"Leave request cannot be updated by the current user. (code: {self.error_code})",
        )
