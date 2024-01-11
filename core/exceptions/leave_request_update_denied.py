from .base import CustomError


class LeaveRequestUpdateDeniedError(CustomError):
    """Raised when a processed leave request is attempted to be updated by an unauthorized user"""

    def __init__(self, error_detail=None, *args, **kwargs):
        self.error_detail = error_detail
        super().__init__(error_code="leave_request_update_denied", *args, **kwargs)

    def default_error_message(self):
        return (
            "Leave request cannot be updated by the current user."
            if not self.error_detail
            else self.error_detail
        )
