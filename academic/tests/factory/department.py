import factory

from academic.models import Department


class DepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Department

    title = factory.Faker("word")
    code = None
