import factory

from academic.tests.factory import CourseFactory, StreamFactory
from faculty.models import Tutor

from .faculty import FacultyFactory


class TutorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tutor

    faculty = factory.SubFactory(FacultyFactory)
    course = factory.SubFactory(CourseFactory)
    stream = factory.SubFactory(StreamFactory)
    batch = factory.Faker("year")
