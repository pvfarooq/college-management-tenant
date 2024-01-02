import factory

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
    password = factory.PostGenerationMethodCall("set_password", "defaultpassword")
    is_active = True
    is_staff = False
    is_superuser = False
    is_student = False
    is_faculty = False


class SuperUserFactory(UserFactory):
    is_superuser = True
    is_staff = True
