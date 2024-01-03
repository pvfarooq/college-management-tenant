import factory

from finance.models import StudentPenalty
from student.tests.factory import StudentFactory


class StudentPenaltyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StudentPenalty

    student = factory.SubFactory(StudentFactory)
    reason = factory.Faker("sentence")
    amount = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    is_paid = factory.Faker("boolean")
