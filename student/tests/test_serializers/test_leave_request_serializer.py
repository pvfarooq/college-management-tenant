from django.test import TestCase
from freezegun import freeze_time

from faculty.tests.factory import TutorFactory
from student.api.serializers import LeaveRequestSerializer

from ..factory import LeaveRequestFactory


@freeze_time("2024-01-01")
class LeaveRequestSerializerTestCase(TestCase):
    def setUp(self):
        self.tutor = TutorFactory()
        self.leave_request = LeaveRequestFactory(
            from_date="2024-01-01", to_date="2024-01-02", tutor=self.tutor
        )
        self.serializer = LeaveRequestSerializer

    def test_leave_request_serializer(self):
        serializer = self.serializer(self.leave_request)
        self.assertEqual(
            serializer.data,
            {
                "id": str(self.leave_request.id),
                "student": self.leave_request.student.id,
                "tutor": self.tutor.id,
                "semester": self.leave_request.semester,
                "status": self.leave_request.status,
                "from_date": str(self.leave_request.from_date),
                "to_date": str(self.leave_request.to_date),
                "reason": self.leave_request.reason,
            },
        )

    def test_leave_request_serializer_with_no_data(self):
        serializer = self.serializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["tutor"][0], "This field is required.")
        self.assertEqual(serializer.errors["from_date"][0], "This field is required.")
        self.assertEqual(serializer.errors["to_date"][0], "This field is required.")
        self.assertEqual(serializer.errors["reason"][0], "This field is required.")
