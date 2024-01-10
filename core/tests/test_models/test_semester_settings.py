from django.test import TestCase

from ..factory import SemesterSettingsFactory


class SemesterSettingsTestCase(TestCase):
    def test_str_representation(self):
        semster_settings = SemesterSettingsFactory()
        self.assertEqual(
            str(semster_settings), f"Semester {semster_settings.semester} Settings"
        )

    def test_unique_semester(self):
        SemesterSettingsFactory(semester=1)
        with self.assertRaises(Exception):
            SemesterSettingsFactory(semester=1)
