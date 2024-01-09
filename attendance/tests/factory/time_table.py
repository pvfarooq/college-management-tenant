import factory
from django.utils import timezone
from factory.fuzzy import FuzzyInteger

from academic.tests.factory import CourseFactory, StreamFactory, SubjectFactory
from attendance.models import TimeTable
from core.enums import Days
from faculty.tests.factory import FacultyFactory

from .time_slot import TimeSlotFactory


class TimeTableFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TimeTable

    batch = FuzzyInteger(1980, timezone.now().year + 1)
    semester = FuzzyInteger(1, 10)
    day = factory.Faker("random_element", elements=Days.weekdays())
    time_slot = factory.SubFactory(TimeSlotFactory)
    course = factory.SubFactory(CourseFactory)
    stream = factory.SubFactory(StreamFactory)
    subject = factory.SubFactory(SubjectFactory)
    faculty = factory.SubFactory(FacultyFactory)
