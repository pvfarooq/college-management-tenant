from enum import Enum


class CourseStatus(str, Enum):
    ENROLLED = "enrolled"
    COMPLETED = "completed"
    DISCONTINUED = "discontinued"
    DIMISSED = "dismissed"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class LeaveRequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
