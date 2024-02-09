from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from faculty.tests.factory import FacultyFactory
from student.tests.factory import StudentFactory
from user.tests.factory import (
    CollegeAdminFactory,
    FacultyUserFactory,
    StudentUserFactory,
    UserFactory,
)

from ..factory import AttendanceFactory, TimeSlotFactory


class AnonymousUserAttendanceViewSetTestCase(APITestCase):
    """Test the AttendanceViewSet as an anonymous user."""

    def test_anonymous_user_list_attendance(self):
        response = self.client.get(reverse("attendance-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )


class CollegeAdminUserAttendanceViewSetTestCase(APITestCase):
    def test_college_admin_user_list_attendance(self):
        user = CollegeAdminFactory()
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse("attendance-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )


class StudentUserAttendanceViewSetTestCase(APITestCase):
    def test_student_user_list_attendance(self):
        user = StudentUserFactory()
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse("attendance-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )


class UserAttendanceViewSetTestCase(APITestCase):
    def test_user_list_attendance(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse("attendance-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )


class TutorAttendanceViewSetTestCase(APITestCase):
    """Test the AttendanceViewSet as a tutor"""

    def setUp(self):
        self.user = FacultyUserFactory()
        self.faculty = FacultyFactory(user=self.user)
        self.attendance = AttendanceFactory(faculty=self.faculty)
        self.list_url = reverse("attendance-list")
        self.client.force_authenticate(user=self.user)

    def test_tutor_list_attendance_without_query_params(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "expected 'batch' and 'semester' in request"
        )

    def test_tutor_list_attendance_with_query_params(self):
        response = self.client.get(
            f"{self.list_url}?batch={self.attendance.batch}&semester={self.attendance.semester}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], str(self.attendance.id))
        self.assertEqual(
            response.data["results"][0]["faculty"], self.faculty.user.get_full_name()
        )
        self.assertEqual(
            response.data["results"][0]["student"], self.attendance.student.name
        )

    def test_tutor_cannot_list_other_tutors_attendance_records(self):
        other_faculty = FacultyFactory()
        other_attendance = AttendanceFactory(faculty=other_faculty)
        response = self.client.get(
            f"{self.list_url}?batch={other_attendance.batch}&semester={other_attendance.semester}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_tutor_retrieve_attendance(self):
        response = self.client.get(
            reverse("attendance-detail", args=[self.attendance.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.attendance.id))
        self.assertEqual(response.data["faculty"], self.faculty.user.get_full_name())
        self.assertEqual(response.data["student"], self.attendance.student.name)

    def test_tutor_cannot_retrieve_other_tutors_attendance(self):
        other_faculty = FacultyFactory()
        other_attendance = AttendanceFactory(faculty=other_faculty)
        response = self.client.get(
            reverse("attendance-detail", args=[other_attendance.id])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_tutor_create_attendance(self):
        time_slot = TimeSlotFactory()
        student = StudentFactory()
        data = {
            "batch": student.batch,
            "semester": 1,
            "date": "2021-01-01",
            "time_slot": time_slot.id,
            "student": student.id,
            "faculty": self.faculty.id,
            "is_present": True,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["student"], student.id)
        self.assertEqual(response.data["faculty"], self.faculty.id)
        self.assertEqual(response.data["time_slot"], time_slot.id)

    def test_tutor_cannot_create_attendance_for_other_faculties(self):
        other_faculty = FacultyFactory()
        time_slot = TimeSlotFactory()
        student = StudentFactory()
        data = {
            "batch": student.batch,
            "semester": 1,
            "date": "2021-01-01",
            "time_slot": time_slot.id,
            "student": student.id,
            "faculty": other_faculty.id,
            "is_present": True,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data["faculty"], other_faculty.id)

    def test_tutor_update_attendance(self):
        data = {"is_present": False}
        response = self.client.patch(
            reverse("attendance-detail", args=[self.attendance.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["is_present"], False)

    def test_tutor_cannot_update_other_tutors_attendance(self):
        other_faculty = FacultyFactory()
        other_attendance = AttendanceFactory(faculty=other_faculty)
        data = {"is_present": False}
        response = self.client.patch(
            reverse("attendance-detail", args=[other_attendance.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_tutor_delete_attendance(self):
        response = self.client.delete(
            reverse("attendance-detail", args=[self.attendance.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
