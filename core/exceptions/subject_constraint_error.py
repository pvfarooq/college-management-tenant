from .base import CustomError


class SubjectConstraintError(CustomError):
    """Raised when a subject constraint is violated.

    Scenarios:
    - When a subject is created with both course and is_common set.
    - When a subject is created with neither course nor is_common set.
    """

    def __init__(self, error_detail=None, *args, **kwargs):
        self.error_detail = error_detail
        super().__init__(error_code="subject_constraint_error", *args, **kwargs)

    def default_error_message(self):
        return (
            "Either 'course' should be set or 'is_common' should be set."
            if not self.error_detail
            else self.error_detail
        )
