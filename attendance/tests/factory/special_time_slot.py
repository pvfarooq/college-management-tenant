import factory

from attendance.models import SpecialTimeSlot
from core.enums import Days

from .time_slot import TimeSlotFactory


class SpecialTimeSlotFactory(TimeSlotFactory):
    class Meta:
        model = SpecialTimeSlot

    day = factory.Faker("random_element", elements=Days.weekdays())
    is_active = True
