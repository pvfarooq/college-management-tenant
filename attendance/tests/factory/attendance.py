import factory
from django.utils import timezone
from factory.fuzzy import FuzzyInteger

from attendance.models import Attendance
from faculty.tests.factory import FacultyFactory
from student.tests.factory import StudentFactory

from .time_slot import TimeSlotFactory


class AttendanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attendance

    batch = FuzzyInteger(1980, timezone.now().year + 1)
    semester = FuzzyInteger(1, 10)
    date = factory.Faker("date_this_year")
    time_slot = factory.SubFactory(TimeSlotFactory)
    student = factory.SubFactory(StudentFactory)
    faculty = factory.SubFactory(FacultyFactory)
    is_present = True
