import factory
from django.utils import timezone

from hostel.models import Hosteller
from user.tests.factory import UserFactory

from .hostel import HostelFactory


class HostellerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Hosteller

    hostel = factory.SubFactory(HostelFactory)
    user = factory.SubFactory(UserFactory)
    room = factory.Faker("pystr", max_chars=10)
    is_dismissed = factory.Faker("pybool")

    @factory.lazy_attribute
    def joining_date(self):
        return timezone.now().date() - timezone.timedelta(days=30)

    @factory.lazy_attribute
    def vacated_date(self):
        return self.joining_date + timezone.timedelta(days=7)
