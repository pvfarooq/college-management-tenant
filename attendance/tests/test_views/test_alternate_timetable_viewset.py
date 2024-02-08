from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from faculty.tests.factory import FacultyFactory
from user.tests.factory import CollegeAdminFactory, UserFactory

from ..factory import AlternateTimeTableFactory, TimeTableFactory


class AnonymousUserAlternateTimeTableViewSetTestCase(APITestCase):
    """Test the AlternateTimeTableViewSet as an anonymous user."""

    def test_anonymous_user_list_alternate_time_tables(self):
        response = self.client.get(reverse("alternate-timetable-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )


class UserAlternateTimeTableViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.list_url = reverse("alternate-timetable-list")
        self.alternate_timetable = AlternateTimeTableFactory(
            start_date="2021-01-01", end_date="2021-01-02"
        )
        self.client.force_authenticate(user=self.user)

    def test_user_list_alternate_time_tables_without_semester_and_batch(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "expected 'batch' and 'semester' in request"
        )

    def test_user_list_alternate_time_tables_with_query_params(self):
        response = self.client.get(
            f"{self.list_url}?batch={self.alternate_timetable.batch}&semester={self.alternate_timetable.semester}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_user_create_alternate_time_table(self):
        data = {
            "start_date": "2021-01-01",
            "end_date": "2021-01-02",
            "time_table": 1,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_user_retrieve_alternate_time_table(self):
        detail_url = reverse(
            "alternate-timetable-detail", kwargs={"pk": self.alternate_timetable.pk}
        )
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["start_date"], "2021-01-01")
        self.assertEqual(response.data["end_date"], "2021-01-02")

    def test_user_update_alternate_time_table(self):
        detail_url = reverse(
            "alternate-timetable-detail", kwargs={"pk": self.alternate_timetable.pk}
        )
        data = {
            "start_date": "2021-01-02",
            "end_date": "2021-01-03",
            "time_table": 1,
        }
        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_user_partial_update_alternate_time_table(self):
        detail_url = reverse(
            "alternate-timetable-detail", kwargs={"pk": self.alternate_timetable.pk}
        )
        data = {
            "start_date": "2021-01-02",
        }
        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_user_delete_alternate_time_table(self):
        detail_url = reverse(
            "alternate-timetable-detail", kwargs={"pk": self.alternate_timetable.pk}
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )


class CollegeAdminAlternateTimeTableViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CollegeAdminFactory()
        self.list_url = reverse("alternate-timetable-list")
        self.alternate_timetable = AlternateTimeTableFactory(
            start_date="2021-01-01", end_date="2021-01-07"
        )
        self.client.force_authenticate(user=self.user)

    def test_college_admin_list_alternate_time_tables_without_semester_and_batch(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "expected 'batch' and 'semester' in request"
        )

    def test_college_admin_list_alternate_time_tables_with_query_params(self):
        response = self.client.get(
            f"{self.list_url}?batch={self.alternate_timetable.batch}&semester={self.alternate_timetable.semester}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_college_admin_create_alternate_time_table(self):
        default_time_table = TimeTableFactory()
        faculty = FacultyFactory()
        data = {
            "start_date": "2021-01-01",
            "end_date": "2021-01-02",
            "default_timetable": default_time_table.id,
            "semester": default_time_table.semester,
            "batch": default_time_table.batch,
            "faculty": faculty.id,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["start_date"], "2021-01-01")
        self.assertEqual(response.data["end_date"], "2021-01-02")

    def test_college_admin_retrieve_alternate_time_table(self):
        detail_url = reverse(
            "alternate-timetable-detail", kwargs={"pk": self.alternate_timetable.pk}
        )
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["start_date"], "2021-01-01")
        self.assertEqual(response.data["end_date"], "2021-01-07")

    def test_college_admin_update_alternate_time_table(self):
        detail_url = reverse(
            "alternate-timetable-detail", kwargs={"pk": self.alternate_timetable.pk}
        )
        time_table = TimeTableFactory()
        data = {
            "start_date": "2021-01-02",
            "end_date": "2021-01-03",
            "default_timetable": time_table.id,
            "faculty": self.alternate_timetable.faculty.id,
            "semester": time_table.semester,
            "batch": time_table.batch,
        }
        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["start_date"], "2021-01-02")
        self.assertEqual(response.data["end_date"], "2021-01-03")

    def test_college_admin_partial_update_alternate_time_table(self):
        detail_url = reverse(
            "alternate-timetable-detail", kwargs={"pk": self.alternate_timetable.pk}
        )
        data = {
            "start_date": "2021-01-02",
        }
        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["start_date"], "2021-01-02")

    def test_college_admin_delete_alternate_time_table(self):
        detail_url = reverse(
            "alternate-timetable-detail", kwargs={"pk": self.alternate_timetable.pk}
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
