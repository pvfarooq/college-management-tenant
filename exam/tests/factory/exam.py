from datetime import datetime, time, timedelta

import factory
from django.utils import timezone
from factory.fuzzy import FuzzyInteger

from academic.tests.factory import (
    CourseFactory,
    DepartmentFactory,
    StreamFactory,
    SubjectFactory,
)
from exam.models import Exam

from .exam_type import ExamTypeFactory


class ExamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Exam

    exam_type = factory.SubFactory(ExamTypeFactory)
    batch = FuzzyInteger(1980, timezone.now().year + 1)
    semester = FuzzyInteger(1, 10)
    department = factory.SubFactory(DepartmentFactory)
    course = factory.SubFactory(CourseFactory)
    stream = factory.SubFactory(StreamFactory)
    subject = factory.SubFactory(SubjectFactory)
    exam_date = factory.Faker("date_this_year")
    venue = factory.Faker("name")
    start_time = time(9, 0, 0).strftime("%H:%M:%S")

    @factory.lazy_attribute
    def end_time(self):
        start_time: str = self.start_time
        end_time = datetime.strptime(start_time, "%H:%M:%S") + timedelta(hours=3)

        if isinstance(end_time, datetime):
            return end_time.time().strftime("%H:%M:%S")
        elif isinstance(end_time, str):
            return end_time
