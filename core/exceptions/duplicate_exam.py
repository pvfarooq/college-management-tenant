from .base import CustomError


class DuplicateExamEntry(CustomError):
    def __init__(self, error_detail=None, *args, **kwargs):
        """Exception raised when attempting to create a duplicate exam."""

        self.error_detail = error_detail
        super().__init__(error_code="duplicate_exam_entry", *args, **kwargs)

    def default_error_message(self):
        return (
            "An exam already exists for the given batch, subject, date, start time and end time."
            if not self.error_detail
            else self.error_detail
        )
