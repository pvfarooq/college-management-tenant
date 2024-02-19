from django.test import TestCase
from django.urls import resolve, reverse
from rest_framework import routers

from student.api.views import LeaveRequestViewSet


class LeaveRequestURLsTestCase(TestCase):
    def setUp(self):
        self.router = routers.SimpleRouter()
        self.router.register(
            "leave-requests", LeaveRequestViewSet, basename="leave-requests"
        )

    def test_leave_request_list_url(self):
        url = reverse("leave-requests-list")
        self.assertEqual(url, "/student/leave-requests/")
        self.assertEqual(resolve(url).func.cls, LeaveRequestViewSet)

    def test_leave_request_detail_url(self):
        url = reverse("leave-requests-detail", kwargs={"pk": "1"})
        self.assertEqual(url, "/student/leave-requests/1/")
        self.assertEqual(resolve(url).func.cls, LeaveRequestViewSet)

    def test_leave_request_create_url(self):
        url = reverse("leave-requests-list")
        self.assertEqual(url, "/student/leave-requests/")
        self.assertEqual(resolve(url).func.cls, LeaveRequestViewSet)

    def test_leave_request_update_url(self):
        url = reverse("leave-requests-detail", kwargs={"pk": "1"})
        self.assertEqual(url, "/student/leave-requests/1/")
        self.assertEqual(resolve(url).func.cls, LeaveRequestViewSet)

    def test_leave_request_delete_url(self):
        url = reverse("leave-requests-detail", kwargs={"pk": "1"})
        self.assertEqual(url, "/student/leave-requests/1/")
        self.assertEqual(resolve(url).func.cls, LeaveRequestViewSet)
