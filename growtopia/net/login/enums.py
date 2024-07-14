__all__ = (
    "AccountType",
    "WebActionType",
)

from enum import Enum, StrEnum


class AccountType(Enum):
    GROWID = 1
    GOOGLE = 2
    APPLE = 3


class WebActionType(StrEnum):
    NEW_SESSION = "/player/login/dashboard"
    CLOSE_SESSION = "/player/validate/close"
    GROWID_VALIDATE = "/player/growid/login/validate"
