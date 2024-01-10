import factory
from factory.fuzzy import FuzzyInteger

from core.models import SemesterSettings


class SemesterSettingsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SemesterSettings

    semester = FuzzyInteger(1, 10)
    start_month_day = factory.Faker("date_this_year")
    end_month_day = factory.Faker("date_this_year")
