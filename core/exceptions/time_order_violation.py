from datetime import time

from .base import CustomError


class TimeOrderViolationError(CustomError):
    """Raised when the given time is less than the reference time"""

    def __init__(self, input_time: time, error_detail=None, *args, **kwargs):
        self.input_time = input_time
        self.error_detail = error_detail
        super().__init__(error_code="time_order_violation", *args, **kwargs)

    def default_error_message(self):
        return (
            f"Given time ({self.input_time}) is less than the reference time."
            if not self.error_detail
            else self.error_detail
        )
