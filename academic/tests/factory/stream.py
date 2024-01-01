import factory

from academic.models import Stream

from .course import CourseFactory


class StreamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Stream

    title = factory.Faker("word")
    course = factory.SubFactory(CourseFactory)
    code = None
