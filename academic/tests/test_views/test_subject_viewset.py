from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user.tests.factory import CollegeAdminFactory, UserFactory

from ..factory import CourseFactory, StreamFactory, SubjectFactory


class AnonymousUserSubjectViewSetTestCase(APITestCase):
    def test_subject_list(self):
        url = reverse("subject-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)


class UserSubjectViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.subject = SubjectFactory()
        self.client.force_authenticate(user=self.user)

    def test_user_lists_subjects(self):
        url = reverse("subject-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_user_retrieve_subject(self):
        url = reverse("subject-detail", kwargs={"pk": self.subject.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.subject.title)
        self.assertEqual(response.data["code"], str(self.subject.code))
        self.assertEqual(response.data["course"], self.subject.course.title)
        self.assertEqual(response.data["is_common"], self.subject.is_common)

    def test_user_create_subject(self):
        url = reverse("subject-list")
        data = {
            "title": "Computer Science",
            "code": "CSB",
            "course": self.subject.course.pk,
            "semester": 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_user_update_subject(self):
        url = reverse("subject-detail", kwargs={"pk": self.subject.pk})
        data = {
            "title": "Computer Science",
            "code": "CSB",
            "course": self.subject.course.pk,
            "semester": 1,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_user_delete_subject(self):
        url = reverse("subject-detail", kwargs={"pk": self.subject.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )


class CollegeAdminSubjectViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CollegeAdminFactory()
        self.subject = SubjectFactory()
        self.client.force_authenticate(user=self.user)

    def test_collegeadmin_list_subjects(self):
        url = reverse("subject-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_collegeadmin_retrieve_subject(self):
        url = reverse("subject-detail", kwargs={"pk": self.subject.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.subject.title)
        self.assertEqual(response.data["code"], str(self.subject.code))
        self.assertEqual(response.data["course"], self.subject.course.title)
        self.assertEqual(response.data["is_common"], self.subject.is_common)

    def test_collegeadmin_create_subject(self):
        url = reverse("subject-list")
        data = {
            "title": "Computer Science",
            "code": "CSB",
            "course": self.subject.course.pk,
            "semester": 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_collegeadmin_update_subject(self):
        url = reverse("subject-detail", kwargs={"pk": self.subject.pk})
        data = {
            "title": "Computer Science",
            "code": "CSB",
            "course": self.subject.course.pk,
            "semester": 1,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_collegeadmin_delete_subject(self):
        url = reverse("subject-detail", kwargs={"pk": self.subject.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubjectViewSetDjangoFilterBackendTestCase(APITestCase):
    """Test Django filter backend in ViewSet"""

    def setUp(self):
        self.list_url = reverse("subject-list")
        self.user = UserFactory()
        course = CourseFactory()
        stream = StreamFactory()
        self.subject = SubjectFactory(course=course, is_elective=True)
        self.subject2 = SubjectFactory(
            stream=stream, is_lab=True, is_common=True, course=None
        )
        self.subject3 = SubjectFactory(
            stream=stream, is_lab=True, is_common=True, course=None
        )
        self.subject4 = SubjectFactory(is_common=True, course=None)
        self.client.force_authenticate(user=self.user)

    def test_subject_filter_by_course(self):
        response = self.client.get(self.list_url, {"course": self.subject.course.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["course"], self.subject.course.title
        )

    def test_subject_filter_by_stream(self):
        response = self.client.get(self.list_url, {"stream": self.subject2.stream.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(
            response.data["results"][0]["stream"], self.subject2.stream.title
        )
        self.assertEqual(
            response.data["results"][1]["stream"], self.subject3.stream.title
        )

    def test_subject_filter_by_is_common(self):
        response = self.client.get(self.list_url, {"is_common": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)
        self.assertEqual(response.data["results"][0]["is_common"], True)
        self.assertEqual(response.data["results"][1]["is_common"], True)
        self.assertEqual(response.data["results"][2]["is_common"], True)

    def test_subject_filter_by_is_elective(self):
        response = self.client.get(self.list_url, {"is_elective": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["is_elective"], True)

    def test_subject_filter_by_is_lab(self):
        response = self.client.get(self.list_url, {"is_lab": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["results"][0]["is_lab"], True)
        self.assertEqual(response.data["results"][1]["is_lab"], True)


class SubjectViewSetSearchFilterBackendTestCase(APITestCase):
    """Test search filter backend in ViewSet"""

    def setUp(self):
        self.list_url = reverse("subject-list")
        self.user = UserFactory()
        self.subject = SubjectFactory(title="Mathematics")
        self.subject2 = SubjectFactory(title="Physics")
        self.client.force_authenticate(user=self.user)

    def test_subject_search_by_title(self):
        response = self.client.get(self.list_url, {"search": "math"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], self.subject.title)

    def test_subject_search_by_code(self):
        response = self.client.get(self.list_url, {"search": "phy"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], self.subject2.title)
        self.assertEqual(response.data["results"][0]["code"], str(self.subject2.code))
