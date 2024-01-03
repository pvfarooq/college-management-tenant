from django.test import TestCase

from ..factory import StudentPenaltyFactory


class StudentPenaltyTestCase(TestCase):
    def test_str_representation(self):
        student_penalty = StudentPenaltyFactory(is_paid=False)
        self.assertEqual(
            str(student_penalty),
            f"{student_penalty.student} - Amount: {student_penalty.amount}",
        )
