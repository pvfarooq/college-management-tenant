from .base import CustomError


class DuplicateTimeTableEntry(CustomError):
    def __init__(self, error_detail=None, *args, **kwargs):
        """Exception raised when attempting to create a duplicate timetable entry."""

        self.error_detail = error_detail
        super().__init__(error_code="duplicate_timetable_entry", *args, **kwargs)

    def default_error_message(self):
        return "A timetable already exists for the given day and time slot."
