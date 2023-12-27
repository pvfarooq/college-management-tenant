from enum import Enum


class AttendanceMode(str, Enum):
    PER_DAY = "per_day"
    PER_PERIOD = "per_period"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
