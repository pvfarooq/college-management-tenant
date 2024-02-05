from django.test import TestCase

from core.exceptions.base import CustomError


class CustomErrorTestCase(TestCase):
    def test_default_error_message(self):
        error_code = "TEST_CODE"
        custom_error = CustomError(error_code)

        expected_message = f"An error occurred with code {error_code}"
        self.assertEqual(custom_error.error_message, expected_message)

    def test_custom_error_message(self):
        error_code = "TEST_CODE"
        custom_message = "Custom error message"
        custom_error = CustomError(error_code, error_message=custom_message)

        self.assertEqual(custom_error.error_message, custom_message)

    def test_string_representation(self):
        error_code = "TEST_CODE"
        custom_message = "Custom error message"
        custom_error = CustomError(error_code, error_message=custom_message)

        expected_string = custom_message
        self.assertEqual(str(custom_error), expected_string)

    def test_default_string_representation(self):
        error_code = "TEST_CODE"
        custom_error = CustomError(error_code)

        expected_string = f"An error occurred with code {error_code}"
        self.assertEqual(str(custom_error), expected_string)

    def test_default_error_message_without_code(self):
        # Test case where error code is not provided
        custom_error = CustomError(None)

        expected_message = "An error occurred with code None"
        self.assertEqual(custom_error.error_message, expected_message)

    def test_default_string_representation_without_code(self):
        # Test case where error code is not provided
        custom_error = CustomError(None)

        expected_string = "An error occurred with code None"
        self.assertEqual(str(custom_error), expected_string)
