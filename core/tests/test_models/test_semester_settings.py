from django.test import TestCase

from ..factory import SemesterSettingsFactory


class SemesterSettingsTestCase(TestCase):
    def test_str(self):
        semster_settings = SemesterSettingsFactory()
        self.assertEqual(str(semster_settings), semster_settings.semester)
