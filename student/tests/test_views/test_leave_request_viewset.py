from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from faculty.tests.factory import FacultyFactory, TutorFactory
from student.enums import LeaveRequestStatus
from student.models import LeaveRequest
from student.tests.factory import StudentFactory
from user.tests.factory import FacultyUserFactory, StudentUserFactory

from ..factory import LeaveRequestFactory


class AnonymousUserLeaveRequestViewSetTestCase(APITestCase):
    """Test the LeaveRequest as an anonymous user."""

    def test_anonymous_user_list_leave_requests(self):
        response = self.client.get(reverse("leave-requests-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )


class FacultyUserLeaveRequestViewSetTestCase(APITestCase):
    def test_faculty_user_list_leave_requests(self):
        user = FacultyUserFactory()
        FacultyFactory(user=user)
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse("leave-requests-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )


class TutorLeaveRequestViewSetTestCase(APITestCase):
    def test_tutor_list_leave_requests(self):
        user = FacultyUserFactory()
        faculty = FacultyFactory(user=user)
        TutorFactory(faculty=faculty)
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse("leave-requests-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )


@freeze_time("2024-01-01")
class StudentUserLeaveRequestViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = StudentUserFactory()
        self.student = StudentFactory(user=self.user)
        self.client.force_authenticate(user=self.user)
        self.leave_request = LeaveRequestFactory(
            student=self.student,
            status=LeaveRequestStatus.PENDING,
            from_date="2024-01-01",
            to_date="2024-01-05",
        )

    def test_list_leave_requests(self):
        response = self.client.get(reverse("leave-requests-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], str(self.leave_request.id))
        self.assertEqual(response.data["results"][0]["student"], self.student.name)
        self.assertEqual(
            response.data["results"][0]["tutor"],
            self.leave_request.tutor.faculty.user.get_full_name(),
        )
        self.assertEqual(
            response.data["results"][0]["from_date"], str(self.leave_request.from_date)
        )
        self.assertEqual(
            response.data["results"][0]["to_date"], str(self.leave_request.to_date)
        )

    def test_retrieve_leave_request(self):
        response = self.client.get(
            reverse("leave-requests-detail", args=[self.leave_request.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.leave_request.id))
        self.assertEqual(response.data["student"], self.student.name)
        self.assertEqual(
            response.data["tutor"],
            self.leave_request.tutor.faculty.user.get_full_name(),
        )
        self.assertEqual(response.data["from_date"], str(self.leave_request.from_date))
        self.assertEqual(response.data["to_date"], str(self.leave_request.to_date))

    def test_create_leave_request(self):
        tutor = TutorFactory()
        data = {
            "semester": 1,
            "from_date": "2024-01-01",
            "to_date": "2024-01-05",
            "reason": "Going home",
            "tutor": tutor.id,
        }
        response = self.client.post(reverse("leave-requests-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["student"], self.student.id)
        self.assertEqual(response.data["tutor"], tutor.id)
        self.assertEqual(response.data["from_date"], data["from_date"])
        self.assertEqual(response.data["to_date"], data["to_date"])
        self.assertEqual(response.data["reason"], data["reason"])
        self.assertEqual(response.data["status"], LeaveRequestStatus.PENDING.value)

    def test_student_cannot_update_leave_request_status(self):
        data = {
            "status": LeaveRequestStatus.APPROVED.value,
        }
        response = self.client.patch(
            reverse("leave-requests-detail", args=[self.leave_request.id]), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], LeaveRequestStatus.PENDING.value)

    def test_update_leave_request(self):
        leave_request = LeaveRequestFactory(
            student=self.student,
            status=LeaveRequestStatus.PENDING,
            from_date="2024-01-01",
            to_date="2024-01-05",
        )
        data = {
            "from_date": "2024-01-02",
        }
        response = self.client.patch(
            reverse("leave-requests-detail", args=[leave_request.id]), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(leave_request.id))
        self.assertEqual(response.data["from_date"], data["from_date"])
        self.assertEqual(response.data["to_date"], str(leave_request.to_date))
        self.assertEqual(response.data["status"], LeaveRequestStatus.PENDING.value)

    def test_delete_leave_request(self):
        leave_request = LeaveRequestFactory(
            student=self.student,
            status=LeaveRequestStatus.PENDING,
            from_date="2024-01-01",
            to_date="2024-01-05",
        )
        response = self.client.delete(
            reverse("leave-requests-detail", args=[leave_request.id])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(LeaveRequest.objects.filter(id=leave_request.id).exists())

    def test_student_cannot_delete_approved_leave_request(self):
        leave_request = LeaveRequestFactory(
            student=self.student,
            status=LeaveRequestStatus.APPROVED,
            from_date="2024-01-01",
            to_date="2024-01-05",
        )
        response = self.client.delete(
            reverse("leave-requests-detail", args=[leave_request.id])
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["detail"], "You can only delete pending leave requests."
        )

    def test_student_cannot_delete_rejected_leave_request(self):
        leave_request = LeaveRequestFactory(
            student=self.student,
            status=LeaveRequestStatus.REJECTED,
            from_date="2024-01-01",
            to_date="2024-01-05",
        )
        response = self.client.delete(
            reverse("leave-requests-detail", args=[leave_request.id])
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["detail"], "You can only delete pending leave requests."
        )

    def test_student_retrieve_other_students_leave_request(self):
        other_student = StudentFactory()
        leave_request = LeaveRequestFactory(
            student=other_student,
            status=LeaveRequestStatus.PENDING,
            from_date="2024-01-01",
            to_date="2024-01-05",
        )
        response = self.client.get(
            reverse("leave-requests-detail", args=[leave_request.id])
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Not found.")

    def test_student_cannot_update_other_students_leave_request(self):
        other_student = StudentFactory()
        leave_request = LeaveRequestFactory(
            student=other_student,
            status=LeaveRequestStatus.PENDING,
            from_date="2024-01-01",
            to_date="2024-01-05",
        )
        data = {
            "from_date": "2024-01-02",
        }
        response = self.client.patch(
            reverse("leave-requests-detail", args=[leave_request.id]), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Not found.")

    def test_student_cannot_create_leave_request_for_other_students(self):
        other_student = StudentFactory()
        tutor = TutorFactory()
        data = {
            "semester": 1,
            "from_date": "2024-01-01",
            "to_date": "2024-01-05",
            "reason": "Going home",
            "tutor": tutor.id,
            "student": other_student.id,
        }
        response = self.client.post(reverse("leave-requests-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data["student"], other_student.id)
        self.assertEqual(response.data["student"], self.student.id)
