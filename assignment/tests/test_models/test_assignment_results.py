from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from core.exceptions import DateOrderViolationError, DuplicateAssignmentResult

from ..factory import AssignmentResultFactory


class AssignmentResultTestCase(TestCase):
    def setUp(self):
        self.assignment_result = AssignmentResultFactory()

    def test_str_representation(self):
        self.assertEqual(
            str(self.assignment_result),
            self.assignment_result.assignment.title
            + " - "
            + self.assignment_result.student.user.username,
        )

    def test_validate_submitted_date(self):
        with self.assertRaises(DateOrderViolationError) as cm:
            AssignmentResultFactory(
                submitted_date=timezone.now().date() + timedelta(days=1)
            )

        self.assertEqual(
            str(cm.exception),
            "Submitted date cannot be in the future",
        )

    def test_validate_unique_assignment_result(self):
        with self.assertRaises(DuplicateAssignmentResult) as cm:
            AssignmentResultFactory(
                assignment=self.assignment_result.assignment,
                student=self.assignment_result.student,
            )

        self.assertEqual(
            str(cm.exception.message),
            "An result with the given assignment and student already exists.",
        )
        self.assertEqual(cm.exception.code, "duplicate_assignment_result_entry")
