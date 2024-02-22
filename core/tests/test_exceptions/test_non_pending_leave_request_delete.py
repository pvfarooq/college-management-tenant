from django.test import TestCase

from core.exceptions import NonPendingLeaveRequestDeletionError


class NonPendingLeaveRequestDeletionErrorTestCase(TestCase):
    def setUp(self):
        self.error_detail = "Some error detail message"
        self.error_code = "non_pending_leave_request_delete_error"

    def test_with_error_detail(self):
        with self.assertRaises(TypeError) as cm:
            raise NonPendingLeaveRequestDeletionError(error_detail=self.error_detail)

        self.assertEqual(
            str(cm.exception),
            "NonPendingLeaveRequestDeletionError() takes no keyword arguments",
        )

    def test_without_error_detail(self):
        with self.assertRaises(NonPendingLeaveRequestDeletionError) as cm:
            raise NonPendingLeaveRequestDeletionError()

        exception = cm.exception
        self.assertEqual(
            exception.error_detail, "You can only delete pending leave requests."
        )
        self.assertEqual(exception.error_code, self.error_code)
