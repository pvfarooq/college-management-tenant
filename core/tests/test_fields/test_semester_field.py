from django.core.exceptions import ValidationError
from django.test import TestCase

from core.fields import SemesterField


class SemesterFieldTest(TestCase):
    def setUp(self):
        self.field = SemesterField()

    def assertValidationError(self, value, expected_error_message):
        with self.assertRaises(ValidationError) as context:
            self.field.validate_semester(value)
        self.assertIn(expected_error_message, str(context.exception))

    def test_valid_semester(self):
        """Test with a valid semester"""
        value = 1
        try:
            self.field.validate_semester(value)
        except ValidationError:
            self.fail("Validation should not raise an error for a valid semester")

    def test_negative_number(self):
        """Test with a negative number"""
        self.assertValidationError(-1, "Semester must be between 1 and 10")

    def test_zero(self):
        """Test with zero"""
        self.assertValidationError(0, "Semester must be between 1 and 10")

    def test_above_range(self):
        """Test with a number above the allowed range"""
        self.assertValidationError(11, "Semester must be between 1 and 10")
