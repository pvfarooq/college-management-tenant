import factory

from core.models import Announcement


class AnnouncementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Announcement

    title = factory.Faker("sentence")
    content = factory.Faker("text")
    image = None
    expire_at = factory.Faker("future_datetime")
