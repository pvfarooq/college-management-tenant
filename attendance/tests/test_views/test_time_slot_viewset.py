from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user.tests.factory import CollegeAdminFactory, UserFactory

from ..factory import TimeSlotFactory


class AnonymousUserTimeSlotViewSetTestCase(APITestCase):
    """Test the TimeSlotViewSet as an anonymous user."""

    def test_anonymous_user_list_time_slots(self):
        response = self.client.get(reverse("timeslot-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )


class UserTimeSlotViewSetTestCase(APITestCase):
    """Test the TimeSlotViewSet as a general user."""

    def setUp(self):
        self.user = UserFactory()
        self.list_url = reverse("timeslot-list")
        self.time_slot = TimeSlotFactory()
        self.client.force_authenticate(user=self.user)

    def test_user_list_time_slots(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_user_create_time_slot(self):
        data = {
            "start_time": "09:00:00",
            "end_time": "10:00:00",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_user_retrieve_time_slot(self):
        detail_url = reverse("timeslot-detail", kwargs={"pk": self.time_slot.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["start_time"], "09:00:00")

    def test_user_update_time_slot(self):
        detail_url = reverse("timeslot-detail", kwargs={"pk": self.time_slot.pk})
        data = {
            "start_time": "10:00:00",
            "end_time": "11:00:00",
        }
        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_user_partial_update_time_slot(self):
        detail_url = reverse("timeslot-detail", kwargs={"pk": self.time_slot.pk})
        data = {
            "start_time": "10:00:00",
        }
        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_user_delete_time_slot(self):
        detail_url = reverse("timeslot-detail", kwargs={"pk": self.time_slot.pk})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )


class CollegeAdminTimeSlotViewSetTestCase(APITestCase):
    """Test the TimeSlotViewSet as a college admin."""

    def setUp(self):
        self.user = CollegeAdminFactory()
        self.list_url = reverse("timeslot-list")
        self.time_slot = TimeSlotFactory()
        self.client.force_authenticate(user=self.user)

    def test_college_admin_list_time_slots(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_college_admin_create_time_slot(self):
        data = {
            "start_time": "09:00:00",
            "end_time": "10:00:00",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["start_time"], "09:00:00")

    def test_college_admin_retrieve_time_slot(self):
        detail_url = reverse("timeslot-detail", kwargs={"pk": self.time_slot.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["start_time"], "09:00:00")

    def test_college_admin_update_time_slot(self):
        detail_url = reverse("timeslot-detail", kwargs={"pk": self.time_slot.pk})
        data = {
            "start_time": "10:00:00",
            "end_time": "11:00:00",
        }
        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["start_time"], "10:00:00")

    def test_college_admin_partial_update_time_slot(self):
        detail_url = reverse("timeslot-detail", kwargs={"pk": self.time_slot.pk})
        data = {
            "start_time": "8:00:00",
        }
        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["start_time"], "08:00:00")

    def test_college_admin_delete_time_slot(self):
        detail_url = reverse("timeslot-detail", kwargs={"pk": self.time_slot.pk})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
