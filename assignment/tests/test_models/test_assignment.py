from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from core.exceptions import DateOrderViolationError

from ..factory import AssignmentFactory


class AssignmentTestCase(TestCase):
    def setUp(self):
        self.assignment = AssignmentFactory()

    def test_str_representation(self):
        self.assertEqual(str(self.assignment), self.assignment.title)

    def test_due_date_less_than_current_date(self):
        with self.assertRaises(DateOrderViolationError) as cm:
            AssignmentFactory(due_date=timezone.now().date() - timedelta(days=1))

        self.assertEqual(
            str(cm.exception),
            "Due date cannot be in the past",
        )
