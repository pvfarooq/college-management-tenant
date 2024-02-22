from datetime import datetime, timedelta

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
    from_date = factory.Faker("date_this_month", after_today=True)
    reason = factory.Faker("text")
    status = factory.Faker(
        "random_element", elements=[status.value for status in LeaveRequestStatus]
    )

    @factory.lazy_attribute
    def to_date(self):
        try:
            return (self.from_date + timedelta(days=5)).strftime("%Y-%m-%d")
        except TypeError:
            end_date_time = datetime.strptime(self.from_date, "%Y-%m-%d") + timedelta(
                days=5
            )
            return end_date_time.strftime("%Y-%m-%d")
