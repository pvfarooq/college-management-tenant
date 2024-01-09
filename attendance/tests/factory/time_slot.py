from datetime import datetime, timedelta

import factory

from attendance.models import TimeSlot


class TimeSlotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TimeSlot

    start_time = factory.Faker("time_object")

    @factory.lazy_attribute
    def end_time(self):
        fixed_date = datetime(2024, 1, 1)
        start_datetime = datetime.combine(fixed_date.date(), self.start_time)
        end_datetime = start_datetime + timedelta(minutes=45)
        return end_datetime.time()
