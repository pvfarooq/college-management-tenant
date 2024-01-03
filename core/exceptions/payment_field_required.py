from finance.enums import PaymentMode

from .base import CustomError


class PaymentFieldRequired(CustomError):
    """Raised when a required field is missing for the given payment mode."""

    def __init__(self, payment_mode: PaymentMode, error_detail=None, *args, **kwargs):
        self.payment_mode = payment_mode
        self.error_detail = error_detail
        super().__init__(error_code="payment_field_required", *args, **kwargs)

    def default_error_message(self):
        return (
            "A required field is missing for the given payment mode."
            if not self.error_detail
            else self.error_detail
        )
