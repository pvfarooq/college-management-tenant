from .base import CustomError


class NonPendingLeaveRequestDeletionError(CustomError):
    def __init__(self, *args, **kwargs):
        self.error_code = "non_pending_leave_request_delete_error"
        self.error_message = "You can only delete pending leave requests."
        super().__init__(self.error_code, self.error_message, *args, **kwargs)

    def default_error_message(self):
        return "You can only delete pending leave requests."
