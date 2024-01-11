from django.core.exceptions import ValidationError


class DuplicateExamResultEntry(ValidationError):
    def __init__(self, message=None, code=None, params=None):
        if message is None:
            message = (
                "An exam result already exists for this student for the given exam."
            )
        super().__init__(message, code, params)
