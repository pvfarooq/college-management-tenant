from django.test import TestCase

from ..factory import AnnouncementFactory


class AnnouncementTestCase(TestCase):
    def test_str(self):
        announcement = AnnouncementFactory()
        self.assertEqual(str(announcement), announcement.title)
