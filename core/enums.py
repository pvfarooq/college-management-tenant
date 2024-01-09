from enum import Enum
from typing import List, Tuple


class AttendanceMode(str, Enum):
    PER_DAY = "per_day"
    PER_PERIOD = "per_period"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Days(str, Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

    @classmethod
    def choices(cls, weekdays_only=True) -> List[Tuple[str, str]]:
        """
        Returns a list of choices as tuples.

        Params:
            weekdays_only (bool): If True, only weekdays will be included in the choices.
        """
        if weekdays_only:
            return [(day.value, day.name) for day in cls if day.value not in ["sunday"]]
        return [(day.value, day.name) for day in cls]

    @classmethod
    def weekdays(cls) -> List[str]:
        return [day.value for day in cls if day.value not in ["sunday"]]
