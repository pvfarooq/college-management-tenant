import factory

from core.enums import Gender
from user.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.LazyAttribute(
        lambda obj: f"{obj.first_name.lower()}.{obj.last_name.lower()}"
    )
    email = factory.LazyAttribute(
        lambda obj: f"{obj.first_name.lower()}.{obj.last_name.lower()}@example.com"
    )
    gender = factory.Faker("random_element", elements=[item.value for item in Gender])
    password = factory.PostGenerationMethodCall("set_password", "defaultpassword")
    is_active = True
    is_staff = False
    is_superuser = False
    is_student = False
    is_faculty = False


class MaleUserFactory(UserFactory):
    gender = Gender.MALE.value


class FemaleUserFactory(UserFactory):
    gender = Gender.FEMALE.value


class SuperUserFactory(UserFactory):
    is_superuser = True
    is_staff = True
