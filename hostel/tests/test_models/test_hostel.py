from django.core.exceptions import ValidationError
from django.test import TestCase

from ..factory import HostelFactory


class HostelTestCase(TestCase):
    def setUp(self):
        self.hostel = HostelFactory()

    def test_hostel_str(self):
        self.assertEqual(
            str(self.hostel), f"{self.hostel.name} ({self.hostel.residency_category})"
        )

    def test_hostel_save(self):
        self.hostel.current_occupancy = 0
        self.hostel.save()

    def test_create_hostel_with_current_occupancy_greater_than_max_capacity(self):
        self.hostel.current_occupancy = self.hostel.max_capacity + 1
        with self.assertRaises(ValidationError):
            self.hostel.save()

    def test_is_full_property(self):
        full_hostel = HostelFactory(max_capacity=100, current_occupancy=100)
        self.assertTrue(full_hostel.is_full)

        with self.assertRaises(ValidationError) as cm:
            new_hostel = HostelFactory(max_capacity=100, current_occupancy=101)

            self.assertEqual(
                str(cm.exception.message),
                f"Hostel - {new_hostel.name} ({new_hostel.residency_category}) is full",
            )
