from .base import CustomError


class CollegeSettingsAlreadyExists(CustomError):
    def __init__(self, *args, **kwargs):
        """Raised when a college settings already exists and a user tries to create another one."""
        super().__init__(error_code="college_settings_exists", *args, **kwargs)

    def default_error_message(self):
        return "A valid college settings already exists. Try updating it instead."
