from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user.tests.factory import CollegeAdminFactory, UserFactory

from ..factory import TimeSlotFactory, TimeTableFactory


class AnonymousUserTimeTableViewSetTestCase(APITestCase):
    """Test the TimeTableViewSet as an anonymous user."""

    def test_anonymous_user_list_time_tables(self):
        response = self.client.get(reverse("timetable-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )


class UserTimeTableViewSetTestCase(APITestCase):
    """Test the TimeTableViewSet as a general user."""

    def setUp(self):
        self.user = UserFactory()
        self.list_url = reverse("timetable-list")
        self.timetable = TimeTableFactory()
        self.client.force_authenticate(user=self.user)

    def test_user_list_time_tables_without_query_params(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "expected 'batch' and 'semester' in request"
        )

    def test_user_list_time_tables_with_query_params(self):
        response = self.client.get(
            f"{self.list_url}?batch={self.timetable.batch}&semester={self.timetable.semester}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_user_create_time_table(self):
        time_slot = TimeSlotFactory()
        data = {
            "batch": 2018,
            "semester": 5,
            "day": "Monday",
            "time_slot": time_slot.id,
            "course": self.timetable.course.id,
            "stream": self.timetable.stream.id,
            "subject": self.timetable.subject.id,
            "faculty": self.timetable.faculty.id,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_user_retrieve_time_table(self):
        detail_url = reverse("timetable-detail", kwargs={"pk": self.timetable.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["batch"], self.timetable.batch)
        self.assertEqual(response.data["semester"], self.timetable.semester)
        self.assertEqual(response.data["day"], self.timetable.day)
        self.assertEqual(
            response.data["time_slot"]["id"], str(self.timetable.time_slot.id)
        )
        self.assertEqual(
            response.data["time_slot"]["start_time"],
            self.timetable.time_slot.start_time,
        )
        self.assertEqual(
            response.data["time_slot"]["end_time"], self.timetable.time_slot.end_time
        )
        self.assertEqual(response.data["course"], self.timetable.course.title)
        self.assertEqual(response.data["stream"], self.timetable.stream.title)
        self.assertEqual(response.data["subject"], self.timetable.subject.title)
        self.assertEqual(
            response.data["faculty"], self.timetable.faculty.user.get_full_name()
        )

    def test_user_update_time_table(self):
        detail_url = reverse("timetable-detail", kwargs={"pk": self.timetable.pk})
        data = {
            "batch": 2019,
            "semester": 6,
            "day": "Tuesday",
            "time_slot": self.timetable.time_slot.id,
            "course": self.timetable.course.id,
            "stream": self.timetable.stream.id,
            "subject": self.timetable.subject.id,
            "faculty": self.timetable.faculty.id,
        }
        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_user_partial_update_time_table(self):
        detail_url = reverse("timetable-detail", kwargs={"pk": self.timetable.pk})
        data = {
            "batch": 2019,
            "semester": 6,
        }
        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_user_delete_time_table(self):
        detail_url = reverse("timetable-detail", kwargs={"pk": self.timetable.pk})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )


class CollegeAdminTimeTableViewSetTestCase(APITestCase):
    def setUp(self):
        self.college_admin = CollegeAdminFactory()
        self.list_url = reverse("timetable-list")
        self.timetable = TimeTableFactory()
        self.client.force_authenticate(user=self.college_admin)

    def test_college_admin_list_time_tables_without_query_params(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "expected 'batch' and 'semester' in request"
        )

    def test_college_admin_list_time_tables_with_query_params(self):
        response = self.client.get(
            f"{self.list_url}?batch={self.timetable.batch}&semester={self.timetable.semester}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_college_admin_create_time_table(self):
        timeslot = TimeSlotFactory()
        data = {
            "batch": 2018,
            "semester": 5,
            "day": "monday",
            "time_slot": timeslot.id,
            "course": self.timetable.course.id,
            "stream": self.timetable.stream.id,
            "subject": self.timetable.subject.id,
            "faculty": self.timetable.faculty.id,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["batch"], data["batch"])
        self.assertEqual(response.data["semester"], data["semester"])
        self.assertEqual(response.data["day"], data["day"])
        self.assertEqual(response.data["time_slot"], data["time_slot"])
        self.assertEqual(response.data["course"], data["course"])
        self.assertEqual(response.data["stream"], data["stream"])
        self.assertEqual(response.data["subject"], data["subject"])
        self.assertEqual(response.data["faculty"], data["faculty"])

    def test_college_admin_retrieve_time_table(self):
        detail_url = reverse("timetable-detail", kwargs={"pk": self.timetable.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["batch"], self.timetable.batch)
        self.assertEqual(response.data["semester"], self.timetable.semester)
        self.assertEqual(response.data["day"], self.timetable.day)
        self.assertEqual(
            response.data["time_slot"]["id"], str(self.timetable.time_slot.id)
        )
        self.assertEqual(
            response.data["time_slot"]["start_time"],
            self.timetable.time_slot.start_time,
        )
        self.assertEqual(
            response.data["time_slot"]["end_time"], self.timetable.time_slot.end_time
        )
        self.assertEqual(response.data["course"], self.timetable.course.title)
        self.assertEqual(response.data["stream"], self.timetable.stream.title)
        self.assertEqual(response.data["subject"], self.timetable.subject.title)
        self.assertEqual(
            response.data["faculty"], self.timetable.faculty.user.get_full_name()
        )

    def test_college_admin_update_time_table(self):
        detail_url = reverse("timetable-detail", kwargs={"pk": self.timetable.pk})
        data = {
            "batch": 2019,
            "semester": 6,
            "day": "tuesday",
            "time_slot": self.timetable.time_slot.id,
            "course": self.timetable.course.id,
            "stream": self.timetable.stream.id,
            "subject": self.timetable.subject.id,
            "faculty": self.timetable.faculty.id,
        }
        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["batch"], data["batch"])
        self.assertEqual(response.data["semester"], data["semester"])
        self.assertEqual(response.data["day"], data["day"])
        self.assertEqual(response.data["time_slot"], data["time_slot"])
        self.assertEqual(response.data["course"], data["course"])
        self.assertEqual(response.data["stream"], data["stream"])
        self.assertEqual(response.data["subject"], data["subject"])
        self.assertEqual(response.data["faculty"], data["faculty"])

    def test_college_admin_partial_update_time_table(self):
        detail_url = reverse("timetable-detail", kwargs={"pk": self.timetable.pk})
        data = {
            "batch": 2019,
            "semester": 6,
        }
        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["batch"], data["batch"])
        self.assertEqual(response.data["semester"], data["semester"])

    def test_college_admin_delete_time_table(self):
        detail_url = reverse("timetable-detail", kwargs={"pk": self.timetable.pk})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
