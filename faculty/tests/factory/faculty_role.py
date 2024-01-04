import factory

from faculty.models import FacultyRole


class FacultyRoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FacultyRole

    title = factory.Faker("job")
    description = factory.Faker("text")
