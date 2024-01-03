import factory

from academic.tests.factory import CourseFactory
from finance.models import CourseFee


class CourseFeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CourseFee

    course = factory.SubFactory(CourseFactory)
    fee = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    valid_from = factory.Faker("past_date")
    valid_to = factory.Faker("future_date")
    is_active = True
