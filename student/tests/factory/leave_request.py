import datetime

import factory
from factory.fuzzy import FuzzyInteger

from faculty.tests.factory import TutorFactory
from student.enums import LeaveRequestStatus
from student.models import LeaveRequest

from .student import StudentFactory


class LeaveRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LeaveRequest

    student = factory.SubFactory(StudentFactory)
    tutor = factory.SubFactory(TutorFactory)
    semester = FuzzyInteger(1, 10)
    from_date = factory.Faker("date")
    reason = factory.Faker("text")
    status = factory.Faker(
        "random_element", elements=[status.value for status in LeaveRequestStatus]
    )

    @factory.lazy_attribute
    def to_date(self):
        return self.from_date + datetime.timedelta(days=5)
