from enum import Enum


class MoneyType(Enum):
    USD = "USD"
    EUR = "EUR"
    UZS = "UZS"


class LangType(Enum):
    UZ = "uz"
    EN = "en"
    KR = "kr"


class StatusEnum(Enum):
    PENDING = "pending"
    APPROVED = "approved"
