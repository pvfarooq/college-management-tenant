from django.test import TestCase

from ..factory import HolidayFactory


class HolidayTestCase(TestCase):
    def test_str(self):
        holiday = HolidayFactory()
        self.assertEqual(str(holiday), holiday.title)
