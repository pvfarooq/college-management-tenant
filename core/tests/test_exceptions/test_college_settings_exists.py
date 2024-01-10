from django.test import TestCase

from core.exceptions import CollegeSettingsAlreadyExists


class CollegeSettingsAlreadyExistsTestCase(TestCase):
    def test_exception(self):
        with self.assertRaises(CollegeSettingsAlreadyExists):
            raise CollegeSettingsAlreadyExists()
