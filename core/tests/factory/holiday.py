import factory

from core.models import Holiday


class HolidayFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Holiday

    title = factory.Faker("sentence")
    description = factory.Faker("text")
    date = factory.Faker("future_date")
