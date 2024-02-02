from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user.tests.factory import CollegeAdminFactory, UserFactory

from ..factory import CourseFactory, StreamFactory


class AnonymousUserStreamViewSetTestCase(APITestCase):
    def test_stream_list(self):
        url = reverse("stream-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)


class UserStreamViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.stream = StreamFactory()
        self.client.force_authenticate(user=self.user)

    def test_user_lists_streams(self):
        url = reverse("stream-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], self.stream.title)
        self.assertEqual(response.data["results"][0]["code"], self.stream.code)
        self.assertEqual(
            response.data["results"][0]["course"], self.stream.course.title
        )

    def test_user_create_stream(self):
        url = reverse("stream-list")
        data = {
            "title": "Computer Science",
            "code": "CSB",
            "course": self.stream.course.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_user_retrieve_stream(self):
        url = reverse("stream-detail", kwargs={"pk": self.stream.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.stream.title)
        self.assertEqual(response.data["code"], self.stream.code)
        self.assertEqual(response.data["course"], self.stream.course.title)

    def test_user_update_stream(self):
        url = reverse("stream-detail", kwargs={"pk": self.stream.pk})
        data = {
            "title": "Computer Science",
            "code": "CS",
            "course": self.stream.course.pk,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_user_delete_stream(self):
        url = reverse("stream-detail", kwargs={"pk": self.stream.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )


class CollegeAdminStreamViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CollegeAdminFactory()
        self.stream = StreamFactory()
        self.client.force_authenticate(user=self.user)

    def test_college_admin_lists_streams(self):
        url = reverse("stream-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], self.stream.title)
        self.assertEqual(response.data["results"][0]["code"], self.stream.code)
        self.assertEqual(
            response.data["results"][0]["course"], self.stream.course.title
        )

    def test_college_admin_create_stream(self):
        url = reverse("stream-list")
        data = {
            "title": "Computer Science",
            "code": "CSB",
            "course": self.stream.course.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["code"], data["code"])
        self.assertEqual(response.data["course"], self.stream.course.id)

    def test_college_admin_retrieve_stream(self):
        url = reverse("stream-detail", kwargs={"pk": self.stream.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.stream.title)
        self.assertEqual(response.data["code"], self.stream.code)
        self.assertEqual(response.data["course"], self.stream.course.title)

    def test_college_admin_update_stream(self):
        url = reverse("stream-detail", kwargs={"pk": self.stream.pk})
        data = {
            "title": "Computer Science",
            "code": "CS",
            "course": self.stream.course.pk,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["code"], data["code"])
        self.assertEqual(response.data["course"], self.stream.course.id)

    def test_college_admin_delete_stream(self):
        url = reverse("stream-detail", kwargs={"pk": self.stream.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class StreamViewSetDjangoFilterBackendTestCase(APITestCase):
    """Test Django filter backend in the ViewSet"""

    def setUp(self):
        self.list_url = reverse("stream-list")
        self.user = UserFactory()
        self.course = CourseFactory()
        self.stream = StreamFactory()
        self.stream2 = StreamFactory(course=self.course)
        self.stream3 = StreamFactory(course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_filter_stream_by_course(self):
        response = self.client.get(self.list_url, {"course": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["results"][0]["course"], self.course.title)
        self.assertEqual(response.data["results"][1]["course"], self.course.title)
