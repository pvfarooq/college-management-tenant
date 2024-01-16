import factory
from django.utils import timezone
from factory.fuzzy import FuzzyInteger

from assignment.models import AssignmentResult
from faculty.tests.factory import FacultyFactory
from student.tests.factory import StudentFactory

from .assignment import AssignmentFactory


class AssignmentResultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AssignmentResult

    assignment = factory.SubFactory(AssignmentFactory)
    student = factory.SubFactory(StudentFactory)
    faculty = factory.SubFactory(FacultyFactory)
    batch = FuzzyInteger(1980, timezone.now().year + 1)
    semester = factory.Faker("random_int", min=1, max=10)
    submitted_date = factory.Faker("date_this_year")
    marks = factory.Faker("random_int", min=1, max=100)
