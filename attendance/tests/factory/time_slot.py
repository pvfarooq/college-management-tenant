import random
from datetime import datetime, timedelta

import factory
from django.utils import timezone

from attendance.models import TimeSlot


class TimeSlotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TimeSlot

    @factory.lazy_attribute
    def start_time(self):
        # Calculate start time as a random time between 8 AM and 6 PM
        start_time = timezone.now() + timedelta(hours=random.randint(8, 18))
        return start_time.time()

    @factory.lazy_attribute
    def end_time(self):
        # Calculate end time as 45 minutes ahead of start time
        start_time = datetime.combine(datetime.today(), self.start_time)
        end_time = start_time + timedelta(minutes=45)
        return end_time.time()
