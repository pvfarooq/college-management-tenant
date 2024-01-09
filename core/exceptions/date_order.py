from datetime import date

from .base import CustomError


class DateOrderViolationError(CustomError):
    """Raised when the given date is less than the reference date"""

    def __init__(self, input_date: date, error_detail=None, *args, **kwargs):
        self.input_date = input_date
        self.error_detail = error_detail
        super().__init__(error_code="date_order_violation", *args, **kwargs)

    def default_error_message(self):
        return (
            f"Given date {self.input_date} is less than the reference date."
            if not self.error_detail
            else self.error_detail
        )
