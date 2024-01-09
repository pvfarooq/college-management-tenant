import factory
from factory.fuzzy import FuzzyInteger

from academic.models import Subject

from .course import CourseFactory
from .stream import StreamFactory


class SubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subject

    title = factory.Faker("sentence", nb_words=4)
    code = factory.Faker("random_number", digits=4)
    course = factory.SubFactory(CourseFactory)
    stream = factory.SubFactory(StreamFactory)
    semester = FuzzyInteger(1, 10)
    is_elective = False
    is_lab = False
    is_active = True
