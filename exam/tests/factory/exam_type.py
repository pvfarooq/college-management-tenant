import factory

from exam.models import ExamType


class ExamTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExamType

    name = factory.Faker("name")
