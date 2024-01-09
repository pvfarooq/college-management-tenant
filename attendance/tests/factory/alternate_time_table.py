import factory
from django.utils import timezone
from factory.fuzzy import FuzzyInteger

from attendance.models import AlternateTimeTable
from faculty.tests.factory import FacultyFactory

from .time_table import TimeTableFactory


class AlternateTimeTableFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AlternateTimeTable

    batch = FuzzyInteger(1980, timezone.now().year + 1)
    semester = FuzzyInteger(1, 10)
    faculty = factory.SubFactory(FacultyFactory)
    start_date = factory.Faker("date_this_year")
    default_timetable = factory.SubFactory(TimeTableFactory)
    reason = factory.Faker("sentence")

    @factory.lazy_attribute
    def end_date(self):
        return self.start_date + timezone.timedelta(days=7)
