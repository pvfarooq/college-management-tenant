import factory

from core.models import SemesterSettings


class SemesterSettingsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SemesterSettings

    semester = factory.Faker(
        "word", ext_word_list=["S{x}".format(x=x) for x in range(1, 9)]
    )
    start_date = factory.Faker("date_this_year")
    end_date = factory.Faker("date_this_year")
