import factory
from django.utils import timezone
from factory.fuzzy import FuzzyInteger

from academic.tests.factory import CourseFactory, StreamFactory
from faculty.models import Tutor

from .faculty import FacultyFactory


class TutorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tutor

    faculty = factory.SubFactory(FacultyFactory)
    course = factory.SubFactory(CourseFactory)
    stream = factory.SubFactory(StreamFactory)
    batch = FuzzyInteger(1980, timezone.now().year + 1)
