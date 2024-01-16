from random import randint

import factory

from hostel.enums import HostelType
from hostel.models import Hostel


class HostelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Hostel

    name = factory.Faker("company")
    block = factory.Faker("pystr", max_chars=10)
    residency_category = factory.Faker(
        "random_element", elements=[item.value for item in HostelType]
    )
    max_capacity = factory.Faker("pyint")
    code = factory.Faker("pystr", max_chars=10)

    @factory.lazy_attribute
    def current_occupancy(self):
        return self.max_capacity - randint(0, self.max_capacity)


class MensHostelFactory(HostelFactory):
    residency_category = HostelType.MENS.value


class WomensHostelFactory(HostelFactory):
    residency_category = HostelType.WOMENS.value
