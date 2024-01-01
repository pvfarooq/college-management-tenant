import factory

from academic.models import Course

from .department import DepartmentFactory


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    title = factory.Faker("word")
    department = factory.SubFactory(DepartmentFactory)
    code = None
    duration = factory.Faker(
        "word", ext_word_list=["{x} years".format(x=x) for x in range(1, 4)]
    )
    auto_promotion = factory.Faker("boolean")
