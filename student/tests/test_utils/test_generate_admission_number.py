from unittest.mock import patch

from django.test import TestCase

from student.models import Student
from student.utils import generate_admission_number

from ..factory import StudentFactory


class GenerateAdmissionNumberTestCase(TestCase):
    def setUp(self):
        self.student1 = StudentFactory(admission_num=1001)
        self.student2 = StudentFactory(admission_num=1002)
        self.student3 = StudentFactory(admission_num=1003)

    def test_generate_admission_number_no_existing_numbers(self):
        # Mock the aggregate method to return None (no existing admission numbers)
        with patch.object(
            Student.objects, "aggregate", return_value={"admission_num__max": None}
        ):
            new_admission_number = generate_admission_number()

        # The generated admission number should be 1
        self.assertEqual(new_admission_number, 1)

    def test_generate_admission_number_existing_numbers(self):
        # Mock the aggregate method to return the maximum admission number
        with patch.object(
            Student.objects, "aggregate", return_value={"admission_num__max": 1003}
        ):
            new_admission_number = generate_admission_number()

        # The generated admission number should be the maximum + 1
        self.assertEqual(new_admission_number, 1004)

    def test_generate_admission_number_existing_numbers_with_gaps(self):
        # Mock the aggregate method to return a non-contiguous range of admission numbers
        with patch.object(
            Student.objects, "aggregate", return_value={"admission_num__max": 1001}
        ):
            new_admission_number = generate_admission_number()

        # The generated admission number should fill the gap (in this case, 1002)
        self.assertEqual(new_admission_number, 1002)
