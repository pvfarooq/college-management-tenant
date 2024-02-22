from django.test import TestCase
from freezegun import freeze_time

from faculty.tests.factory import TutorFactory
from student.api.serializers import LeaveRequestListSerializer

from ..factory import LeaveRequestFactory


@freeze_time("2024-01-01")
class TimeTableListSerializerTestCase(TestCase):
    def setUp(self):
        self.tutor = TutorFactory()
        self.leave_request = LeaveRequestFactory(
            from_date="2024-01-01", to_date="2024-01-02", tutor=self.tutor
        )
        self.serializer = LeaveRequestListSerializer

    def test_leave_request_list_serializer(self):
        serializer = self.serializer(self.leave_request)
        self.assertEqual(
            serializer.data,
            {
                "id": str(self.leave_request.id),
                "student": self.leave_request.student.name,
                "tutor": self.tutor.faculty.user.get_full_name(),
                "semester": self.leave_request.semester,
                "status": self.leave_request.status,
                "from_date": str(self.leave_request.from_date),
                "to_date": str(self.leave_request.to_date),
                "reason": self.leave_request.reason,
            },
        )
