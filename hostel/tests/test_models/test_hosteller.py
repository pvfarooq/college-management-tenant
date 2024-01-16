from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase

from user.tests.factory import FemaleUserFactory, MaleUserFactory

from ..factory import HostellerFactory, MensHostelFactory, WomensHostelFactory


class HostellerTestCase(TestCase):
    def setUp(self):
        self.male_user = MaleUserFactory()
        self.mens_hostel = MensHostelFactory()
        self.hosteller = HostellerFactory(hostel=self.mens_hostel, user=self.male_user)

    def test_hosteller_str(self):
        self.assertEqual(
            str(self.hosteller), f"{self.hosteller.user} - {self.hosteller.hostel}"
        )

    def test_create_hosteller_exceeding_hostel_capacity(self):
        full_womens_hostel = WomensHostelFactory(
            max_capacity=100, current_occupancy=100
        )
        female_user = FemaleUserFactory()

        with self.assertRaises(ValidationError) as cm:
            HostellerFactory(hostel=full_womens_hostel, user=female_user)

        self.assertEqual(
            str(cm.exception.message),
            f"Hostel - {full_womens_hostel.name} ({full_womens_hostel.residency_category}) is full",
        )

    def test_validate_gender(self):
        male_user = MaleUserFactory()
        womens_hostel = WomensHostelFactory()
        with self.assertRaises(ValidationError) as cm:
            HostellerFactory(hostel=womens_hostel, user=male_user)
        self.assertEqual(
            str(cm.exception.message),
            f"You cannot add a {male_user.gender} person to the {womens_hostel.residency_category.lower()}'s hostel",
        )

    def test_validate_unique_hosteller(self):
        with self.assertRaises(ValidationError) as cm:
            HostellerFactory(user=self.male_user, hostel=self.mens_hostel)
        self.assertEqual(
            str(cm.exception.message), f"{self.male_user} is already a hosteller"
        )

    def test_vacated_date_in_future(self):
        with self.assertRaises(ValidationError) as cm:
            hosteller = HostellerFactory(
                hostel=MensHostelFactory(),
                user=MaleUserFactory(),
                vacated_date=date.today() + timedelta(days=10),
            )
            hosteller.save()
        self.assertEqual(
            str(cm.exception.message), "Vacated date cannot be in the future"
        )

    def test_joining_date_in_future(self):
        with self.assertRaises(ValidationError) as cm:
            hosteller = HostellerFactory(
                hostel=MensHostelFactory(),
                user=MaleUserFactory(),
                joining_date=date.today() + timedelta(days=10),
                vacated_date=None,
            )
            hosteller.save()
        self.assertEqual(
            str(cm.exception.message), "Joining date cannot be in the future"
        )

    def test_joining_date_after_vacated_date(self):
        with self.assertRaises(ValidationError) as cm:
            hosteller = HostellerFactory(
                hostel=MensHostelFactory(),
                user=MaleUserFactory(),
                joining_date=date.today() - timedelta(days=30),
                vacated_date=date.today() - timedelta(days=31),
            )
            hosteller.save()
        self.assertEqual(
            str(cm.exception.message), "Joining date cannot be after vacated date"
        )
