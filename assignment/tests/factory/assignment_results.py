import factory

from faculty.tests.factory import FacultyFactory
from student.tests.factory import StudentFactory

from .assignment import AssignmentFactory


class AssignmentResultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "assignment.AssignmentResult"

    assignment = factory.SubFactory(AssignmentFactory)
    student = factory.SubFactory(StudentFactory)
    faculty = factory.SubFactory(FacultyFactory)
    batch = factory.Faker("year")
    semester = factory.Faker("random_int", min=1, max=10)
    submitted_date = factory.Faker("date_this_year")
    marks = factory.Faker("random_int", min=1, max=100)
