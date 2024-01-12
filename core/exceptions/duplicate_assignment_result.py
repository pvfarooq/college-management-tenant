from django.core.exceptions import ValidationError


class DuplicateAssignmentResult(ValidationError):
    def __init__(self, message=None, code=None, params=None):
        if message is None:
            message = "An result with the given assignment and student already exists."
        if code is None:
            code = "duplicate_assignment_result_entry"
        super().__init__(message, code, params)
