from enum import Enum

from core.enums import Gender


class HostelType(str, Enum):
    MENS = "mens"
    WOMENS = "womens"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    def gender_check(self, gender: str) -> bool:
        """
        Check if the given gender is allowed in the specified hostel type.
        """
        return (self == HostelType.MENS and gender == Gender.MALE.value) or (
            self == HostelType.WOMENS and gender == Gender.FEMALE.value
        )
