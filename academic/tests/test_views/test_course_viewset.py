from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user.tests.factory import CollegeAdminFactory, UserFactory

from ..factory import CourseFactory, DepartmentFactory


class AnonymousUserCourseViewSetTestCase(APITestCase):
    def test_course_list(self):
        url = reverse("course-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)


class UserCourseViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.course = CourseFactory()
        self.client.force_authenticate(user=self.user)

    def test_user_lists_courses(self):
        url = reverse("course-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_user_create_course(self):
        url = reverse("course-list")
        data = {
            "title": "Computer Science",
            "code": "CS",
            "duration": "3 years",
            "auto_promotion": True,
            "department": self.course.department.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_user_retrieve_course(self):
        url = reverse("course-detail", kwargs={"pk": self.course.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.course.title)

    def test_user_update_course(self):
        url = reverse("course-detail", kwargs={"pk": self.course.pk})
        data = {
            "title": "Computer Science",
            "code": "CS",
            "duration": "3 years",
            "auto_promotion": True,
            "department": self.course.department.pk,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_user_delete_course(self):
        url = reverse("course-detail", kwargs={"pk": self.course.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )


class CollegeAdminCourseViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CollegeAdminFactory()
        self.course = CourseFactory()
        self.client.force_authenticate(user=self.user)

    def test_college_admin_lists_courses(self):
        url = reverse("course-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], self.course.title)
        self.assertEqual(
            response.data["results"][0]["department"]["title"],
            self.course.department.title,
        )

    def test_college_admin_create_course(self):
        url = reverse("course-list")
        data = {
            "title": "Computer Science",
            "code": "CS",
            "duration": "3 years",
            "auto_promotion": True,
            "department": self.course.department.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Computer Science")

    def test_college_admin_retrieve_course(self):
        url = reverse("course-detail", kwargs={"pk": self.course.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.course.title)
        self.assertEqual(
            response.data["department"]["title"], self.course.department.title
        )

    def test_college_admin_update_course(self):
        url = reverse("course-detail", kwargs={"pk": self.course.pk})
        data = {
            "title": "Computer Science",
            "code": "CS",
            "duration": "3 years",
            "auto_promotion": True,
            "department": self.course.department.pk,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Computer Science")
        self.assertEqual(response.data["department"], self.course.department.id)

    def test_college_admin_delete_course(self):
        url = reverse("course-detail", kwargs={"pk": self.course.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CourseViewSetDjangoFilterBackendTestCase(APITestCase):
    """Test Django filter backend in ViewSet"""

    def setUp(self):
        self.list_url = reverse("course-list")
        self.user = UserFactory()
        department = DepartmentFactory()
        self.course = CourseFactory(department=department, auto_promotion=True)
        self.course2 = CourseFactory(department=department, auto_promotion=True)
        self.course3 = CourseFactory(auto_promotion=False)
        self.client.force_authenticate(user=self.user)

    def test_filter_course_by_department(self):
        response = self.client.get(
            self.list_url, {"department": self.course.department.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(
            response.data["results"][0]["department"]["title"],
            self.course.department.title,
        )

    def test_filter_course_by_autopromotion(self):
        response = self.client.get(self.list_url, {"auto_promotion": False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["auto_promotion"], False)
        self.assertEqual(response.data["results"][0]["title"], self.course3.title)


class CourseViewSetSearchFilterBackendTestCase(APITestCase):
    """Test search filter backend in ViewSet"""

    def setUp(self):
        self.list_url = reverse("course-list")
        self.user = UserFactory()
        self.course = CourseFactory(title="Computer Science", code="CS")
        self.course2 = CourseFactory(title="Electrical Engineering", code="EE")
        self.client.force_authenticate(user=self.user)

    def test_search_course_by_title(self):
        response = self.client.get(self.list_url, {"search": "Computer Science"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], "Computer Science")
        self.assertEqual(response.data["results"][0]["code"], "CS")

    def test_search_course_by_code(self):
        response = self.client.get(self.list_url, {"search": "CS"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["code"], "CS")
        self.assertEqual(response.data["results"][0]["title"], "Computer Science")
