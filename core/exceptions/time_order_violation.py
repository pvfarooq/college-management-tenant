from datetime import time

from .base import CustomError


class TimeOrderViolationError(CustomError):
    """Raised when the given time is less than the reference time"""

    def __init__(
        self, start_time: time, end_time: time, error_detail=None, *args, **kwargs
    ):
        self.start_time = start_time
        self.end_time = end_time
        self.error_detail = error_detail
        super().__init__(error_code="time_order_violation", *args, **kwargs)

    def default_error_message(self):
        return (
            f"start time '{self.start_time}' must be less than the end time '{self.end_time}'"
            if not self.error_detail
            else self.error_detail
        )
