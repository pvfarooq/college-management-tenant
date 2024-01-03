class CustomError(Exception):
    def __init__(self, error_code, error_message=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_code = error_code
        self.error_message = error_message or self.default_error_message()

    def default_error_message(self):
        return f"An error occurred with code {self.error_code}"

    def __str__(self):
        return f"{self.error_message} (code: {self.error_code})"
