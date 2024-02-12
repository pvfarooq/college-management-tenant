from .base import CustomError


class AttendanceEditWindowClosed(CustomError):
    def __init__(self, *args, **kwargs):
        """Raised when a faculty tries to edit attendance after the window has closed."""
        super().__init__(error_code="attendance_edit_window_closed", *args, **kwargs)

    def default_error_message(self):
        return "Attendance edit window has closed after the allowed days.Contact admin for further assistance."
