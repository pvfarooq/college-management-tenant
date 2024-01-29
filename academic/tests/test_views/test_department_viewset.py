from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user.tests.factory import CollegeAdminFactory, UserFactory

from ..factory import DepartmentFactory


class AnonymousUserDepartmentViewSetTestCase(APITestCase):
    def test_anonymous_user_list_departments(self):
        response = self.client.get(reverse("department-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)


class UserDepartmentViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.department = DepartmentFactory(title="Information Technology", code="IT")
        self.list_url = reverse("department-list")
        self.client.force_authenticate(user=self.user)

    def test_user_list_departments(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_user_create_department(self):
        data = {
            "title": "Computer Science",
            "code": "CS",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_user_retrieve_department(self):
        detail_url = reverse("department-detail", kwargs={"pk": self.department.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Information Technology")

    def test_user_update_department(self):
        detail_url = reverse("department-detail", kwargs={"pk": self.department.pk})
        data = {
            "title": "Computer Science",
            "code": "CS",
        }
        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_user_delete_department(self):
        detail_url = reverse("department-detail", kwargs={"pk": self.department.pk})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )


class CollegeAdminDepartmentViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CollegeAdminFactory()
        self.department = DepartmentFactory(title="Information Technology", code="IT")
        self.list_url = reverse("department-list")
        self.client.force_authenticate(user=self.user)

    def test_college_admin_list_departments(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_college_admin_create_department(self):
        data = {
            "title": "Computer Science",
            "code": "CS",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Computer Science")

    def test_college_admin_retrieve_department(self):
        detail_url = reverse("department-detail", kwargs={"pk": self.department.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Information Technology")

    def test_college_admin_update_department(self):
        detail_url = reverse("department-detail", kwargs={"pk": self.department.pk})
        data = {
            "title": "Computer Science",
            "code": "CS",
        }
        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Computer Science")

    def test_college_admin_partial_update_department(self):
        detail_url = reverse("department-detail", kwargs={"pk": self.department.pk})
        data = {
            "title": "Computer Science",
        }
        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Computer Science")

    def test_college_admin_delete_department(self):
        detail_url = reverse("department-detail", kwargs={"pk": self.department.pk})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
