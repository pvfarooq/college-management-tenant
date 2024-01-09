from .base import CustomError


class DuplicateTimeTableEntry(CustomError):
    def __init__(self, error_detail=None, *args, **kwargs):
        """Exception raised when attempting to create a duplicate timetable entry."""

        self.error_detail = error_detail
        super().__init__(error_code="duplicate_timetable_entry", *args, **kwargs)

    def default_error_message(self):
        return "A timetable already exists for the given day and time slot."


class DuplicateAlternateTimeTableEntry(CustomError):
    def __init__(self, error_detail=None, *args, **kwargs):
        """Exception raised when attempting to create a duplicate alternate timetable entry."""

        self.error_detail = error_detail
        super().__init__(
            error_code="duplicate_alternate_timetable_entry", *args, **kwargs
        )

    def default_error_message(self):
        return "An alternate timetable already exists for the given date range."
