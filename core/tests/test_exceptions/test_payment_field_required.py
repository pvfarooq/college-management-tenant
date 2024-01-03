from django.test import TestCase

from core.exceptions import PaymentFieldRequired
from finance.enums import PaymentMode


class PaymentFieldRequiredTests(TestCase):
    def test_payment_field_required_creation(self):
        payment_mode = PaymentMode.CASH
        error_detail = "Missing field: example_field"
        payment_field_required = PaymentFieldRequired(payment_mode, error_detail)

        self.assertEqual(payment_field_required.payment_mode, payment_mode)
        self.assertEqual(payment_field_required.error_detail, error_detail)

    def test_payment_field_required_default_message(self):
        payment_mode = PaymentMode.CASH
        payment_field_required = PaymentFieldRequired(payment_mode)

        expected_message = "A required field is missing for the given payment mode. (code: payment_field_required)"
        self.assertEqual(str(payment_field_required), expected_message)

    def test_payment_field_required_custom_message(self):
        payment_mode = PaymentMode.CHALLAN
        error_detail = "Missing field: example_field"
        payment_field_required = PaymentFieldRequired(payment_mode, error_detail)

        expected_message = error_detail + " (code: payment_field_required)"
        self.assertEqual(str(payment_field_required), expected_message)
