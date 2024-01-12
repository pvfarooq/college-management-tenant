import factory
from django.utils import timezone
from factory.fuzzy import FuzzyInteger

from academic.tests.factory import SubjectFactory
from assignment.models import Assignment
from faculty.tests.factory import FacultyFactory


class AssignmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Assignment

    title = factory.Faker("name")
    batch = FuzzyInteger(1980, timezone.now().year + 1)
    semester = FuzzyInteger(1, 10)
    faculty = factory.SubFactory(FacultyFactory)
    subject = factory.SubFactory(SubjectFactory)
    description = factory.Faker("text")

    @factory.lazy_attribute
    def due_date(self):
        return timezone.now().date() + timezone.timedelta(days=10)
