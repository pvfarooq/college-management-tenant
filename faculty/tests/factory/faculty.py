import factory

from academic.tests.factory import DepartmentFactory
from faculty.models import Faculty
from user.tests.factory import UserFactory

from .faculty_role import FacultyRoleFactory


class FacultyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Faculty

    user = factory.SubFactory(UserFactory)
    department = factory.SubFactory(DepartmentFactory)
    faculty_code = factory.Faker("uuid4")
    joining_date = factory.Faker("past_date")

    @factory.post_generation
    def roles(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for role in extracted:
                self.roles.add(role)
        elif extracted == []:
            return
        else:
            default_role = FacultyRoleFactory()
            self.roles.add(default_role)
