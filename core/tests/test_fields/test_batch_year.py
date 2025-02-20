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
            field.validate(value, field)
        except ValidationError:
            self.fail("Validation should not raise an error for a valid batch year")

    def test_invalid_low_batch_year(self):
        """Test with an invalid batch year below the allowed range"""
        field = BatchYearField()
        value = 1979
        with self.assertRaises(ValidationError) as context:
            field.validate(value, field)

        expected_error_message = "Batch year must be between 1980 and "
        expected_error_message += f"{datetime.datetime.now().year + 1}"
        self.assertIn(expected_error_message, str(context.exception))

    def test_invalid_high_batch_year(self):
        """Test with an invalid batch year above the allowed range"""
        field = BatchYearField()
        value = datetime.datetime.now().year + 2
        with self.assertRaises(ValidationError) as context:
            field.validate(value, field)

        expected_error_message = "Batch year must be between 1980 and "
        expected_error_message += f"{datetime.datetime.now().year + 1}"
        self.assertIn(expected_error_message, str(context.exception))

    def test_db_type_method(self):
        """Test the db_type method"""
        field = BatchYearField()
        self.assertEqual(
            field.db_type(None),
            "smallint",
        )

    def test_db_check_method(self):
        """Test the db_check method"""
        field = BatchYearField()
        self.assertEqual(
            field.db_check(None),
            '"batch" >= 1980 AND "batch" <= extract(year from current_date) + 1',
        )
