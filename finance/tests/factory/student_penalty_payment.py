import factory

from finance.enums import PaymentMode
from finance.models import StudentPenaltyPayment

from .student_penalty import StudentPenaltyFactory


class StudentPenaltyPaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StudentPenaltyPayment

    penalty = factory.SubFactory(StudentPenaltyFactory)
    paid_amount = factory.Faker(
        "pydecimal", left_digits=5, right_digits=2, positive=True
    )
    payment_mode = factory.Faker(
        "random_element", elements=[item.value for item in PaymentMode]
    )
    txn_id = factory.Faker("uuid4")
    reference_number = factory.Faker("uuid4")
    remarks = factory.Faker("sentence")
