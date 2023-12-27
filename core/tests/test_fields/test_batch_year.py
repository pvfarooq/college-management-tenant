import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from core.fields import BatchYearField


class BatchYearFieldTest(TestCase):
    def test_valid_batch_year(self):
        """Test with a valid batch year"""
        field = BatchYearField()
        value = 2022
        try:
            field.validate_year(value)
        except ValidationError:
            self.fail("Validation should not raise an error for a valid batch year")

    def test_invalid_low_batch_year(self):
        """Test with an invalid batch year below the allowed range"""
        field = BatchYearField()
        value = 1979
        with self.assertRaises(ValidationError) as context:
            field.validate_year(value)

        expected_error_message = "Batch year must be between 1980 and "
        expected_error_message += f"{datetime.datetime.now().year + 1}"
        self.assertIn(expected_error_message, str(context.exception))

    def test_invalid_high_batch_year(self):
        """Test with an invalid batch year above the allowed range"""
        field = BatchYearField()
        value = datetime.datetime.now().year + 2
        with self.assertRaises(ValidationError) as context:
            field.validate_year(value)

        expected_error_message = "Batch year must be between 1980 and "
        expected_error_message += f"{datetime.datetime.now().year + 1}"
        self.assertIn(expected_error_message, str(context.exception))
