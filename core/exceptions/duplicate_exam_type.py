from django.core.exceptions import ValidationError


class DuplicateExamTypeEntry(ValidationError):
    def __init__(self, message=None, code=None, params=None):
        if message is None:
            message = "An exam type with the given name already exists."
        super().__init__(message, code, params)
