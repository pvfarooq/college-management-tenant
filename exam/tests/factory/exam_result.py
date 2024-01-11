import factory
from django.utils import timezone
from factory.fuzzy import FuzzyInteger

from academic.tests.factory import SubjectFactory
from exam.models import ExamResult
from faculty.tests.factory import FacultyFactory
from student.tests.factory import StudentFactory

from .exam import ExamFactory


class ExamResultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExamResult

    exam = factory.SubFactory(ExamFactory)
    student = factory.SubFactory(StudentFactory)
    subject = factory.SubFactory(SubjectFactory)
    faculty = factory.SubFactory(FacultyFactory)
    marks = factory.Faker("pyint", min_value=0, max_value=100)
    grade = factory.Faker("pystr", max_chars=2)
    remarks = factory.Faker("pystr", max_chars=50)
    batch = FuzzyInteger(1980, timezone.now().year + 1)
    semester = FuzzyInteger(1, 10)
