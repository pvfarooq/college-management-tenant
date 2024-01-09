from .base import CustomError


class DuplicateAttendanceEntry(CustomError):
    def __init__(self, error_detail=None, *args, **kwargs):
        """Exception raised when attempting to create a duplicate attendance."""

        self.error_detail = error_detail
        super().__init__(error_code="duplicate_attendance_entry", *args, **kwargs)

    def default_error_message(self):
        return "An attendance already exists for the given date, time slot and student."
