from enum import Enum


class CourseStatus(str, Enum):
    ENROLLED = "enrolled"
    COMPLETED = "completed"
    DISCONTINUED = "discontinued"
    DIMISSED = "dismissed"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
