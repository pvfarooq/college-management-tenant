from enum import Enum
from typing import List


class PaymentMode(str, Enum):
    CASH = "CASH"
    CHALLAN = "CHALLAN"
    UPI = "UPI"
    ONLINE = "ONLINE"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def online_payment_modes(cls) -> List[str]:
        return [cls.UPI.value, cls.ONLINE.value]
