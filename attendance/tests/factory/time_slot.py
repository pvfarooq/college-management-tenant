from datetime import datetime, time, timedelta

import factory

from attendance.models import TimeSlot


class TimeSlotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TimeSlot

    start_time = time(9, 0, 0).strftime("%H:%M:%S")

    @factory.lazy_attribute
    def end_time(self):
        start_time: str = self.start_time
        end_time = datetime.strptime(start_time, "%H:%M:%S") + timedelta(minutes=45)

        if isinstance(end_time, datetime):
            return end_time.time().strftime("%H:%M:%S")
        elif isinstance(end_time, str):
            return end_time
