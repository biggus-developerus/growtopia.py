__all__ = (
    "EventID",
    "Colour",
)

from enum import Enum
from typing import Any


class EventID(Enum):
    """
    An enumeration of all dispatchable events.
    """

    # General events (not related to ENet / Growtopia)
    ON_UNHANDLED = "on_unhandled"
    ON_CLEANUP = "on_cleanup"
    ON_READY = "on_ready"

    # ENet events
    ON_CONNECT = "on_connect"
    ON_DISCONNECT = "on_disconnect"
    ON_RECEIVE = "on_receive"

    # Packet events
    ON_HELLO = "on_hello"
    ON_MALFORMED_PACKET = "on_malformed_packet"
    ON_LOGIN_REQUEST = "on_login_request"
    ON_ACTION_QUIT = "on_quit"
    ON_DIALOG_RETURN = "on_dialog_return"

    @classmethod
    def _missing_(cls, _: object) -> Any:
        return cls("on_unhandled")


class Colour(str, Enum):
    """
    An enumeration of all text colours that can be used.
    """

    DEFAULT = "``"
    WHITE = "`0"
    SKY_BLUE = "`1"
    GREEN = "`2"
    PALE_BLUE = "`3"
    RED = "`4"
    LIGHT_PINK = "`5"
    TAN = "`6"
    GREY = "`7"
    ORANGE = "`8"
    YELLOW = "`9"
    BLACK = "`b"
    PASTEL_RED = "`@"
    DARK_PINK = "`#"
    PASTEL_YELLOW = "`$"
    PASTEL_GREEN = "`^"
