from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

from ..factory import StudentFactory


class StudentTestCase(TestCase):
    """Test cases for Student model"""

    def setUp(self):
        self.student = StudentFactory()

    def test_str(self):
        """Test str method of Student model"""
        self.assertEqual(str(self.student), self.student.name)

    def test_unique_admission_number(self):
        """Test admission_number field is unique"""
        with self.assertRaises(IntegrityError):
            StudentFactory(admission_num=self.student.admission_num)

    def test_course_completion_date_not_less_than_enrolled_date(self):
        """Test course_completion_date is not less than enrolled_date"""

        enrolled_date = timezone.now().date()
        with self.assertRaises(ValidationError) as context:
            StudentFactory(
                enrolled_date=enrolled_date,
                course_completion_date=enrolled_date + timezone.timedelta(days=1),
            )
        self.assertEqual(
            context.exception.messages[0],
            "Course completion date cannot be earlier than enrolled date.",
        )

    def test_discontinued_date_not_less_than_enrolled_date(self):
        """Test discontinued_date is not less than enrolled_date"""

        enrolled_date = timezone.now().date()
        with self.assertRaises(ValidationError) as context:
            StudentFactory(
                enrolled_date=enrolled_date,
                discontinued_date=enrolled_date + timezone.timedelta(days=1),
            )
        self.assertEqual(
            context.exception.messages[0],
            "Discontinued date cannot be earlier than enrolled date.",
        )

    def test_dismised_date_not_less_than_enrolled_date(self):
        """Test dismissed_date is not less than enrolled_date"""

        enrolled_date = timezone.now().date()
        with self.assertRaises(ValidationError) as context:
            StudentFactory(
                enrolled_date=enrolled_date,
                dismissed_date=enrolled_date + timezone.timedelta(days=1),
            )
        self.assertEqual(
            context.exception.messages[0],
            "Dismissed date cannot be earlier than enrolled date.",
        )
