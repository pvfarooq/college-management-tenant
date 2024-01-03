from django.test import TestCase

from core.exceptions import PaymentFieldRequired
from finance.enums import PaymentMode

from ..factory import StudentPenaltyPaymentFactory


class StudentPenaltyTestCase(TestCase):
    def test_str_representation(self):
        student_penalty_payment = StudentPenaltyPaymentFactory()
        self.assertEqual(
            str(student_penalty_payment),
            f"{student_penalty_payment.penalty.student} - Amount: {student_penalty_payment.paid_amount}",
        )

    def test_txn_id_is_not_required_for_cash_payment_mode(self):
        student_penalty_payment = StudentPenaltyPaymentFactory(
            payment_mode=PaymentMode.CASH.value, txn_id=None
        )
        self.assertIsNone(student_penalty_payment.txn_id)

    def test_reference_number_is_required_for_challan_payment_mode(self):
        with self.assertRaises(PaymentFieldRequired) as context:
            StudentPenaltyPaymentFactory(
                payment_mode=PaymentMode.CHALLAN.value, reference_number=None
            )
        self.assertEqual(
            str(context.exception),
            "Reference number is required for challan payments. (code: payment_field_required)",
        )

    def test_txn_id_is_required_for_electronic_payment_mode(self):
        with self.assertRaises(PaymentFieldRequired) as context:
            StudentPenaltyPaymentFactory(
                payment_mode=PaymentMode.UPI.value, txn_id=None
            )
        self.assertEqual(
            str(context.exception),
            "Transaction ID is required for electronic payments. (code: payment_field_required)",
        )

    def test_reference_number_is_not_required_for_electronic_payment_mode(self):
        student_penalty_payment = StudentPenaltyPaymentFactory(
            payment_mode=PaymentMode.UPI.value, reference_number=None
        )
        self.assertIsNone(student_penalty_payment.reference_number)
