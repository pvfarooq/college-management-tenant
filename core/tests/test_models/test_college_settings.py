from django.test import TestCase

from ..factory import CollegeSettingsFactory


class CollegeSettingsTestCase(TestCase):
    def test_str(self):
        college_settings = CollegeSettingsFactory()
        self.assertEqual(str(college_settings), "College Settings")
