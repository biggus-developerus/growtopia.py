__all__ = ("EventID",)

from enum import Enum
from typing import Any


class EventID(Enum):
    """
    An enumeration of all dispatchable events.
    """

    # General events (not related to ENet / Growtopia)
    ON_UNHANDLED = "on_unhandled"
    ON_CLEANUP = "on_cleanup"

    # ENet events
    ON_CONNECT = "on_connect"
    ON_DISCONNECT = "on_disconnect"
    ON_RECEIVE = "on_receive"

    # Packet events
    ON_HELLO = "on_hello"
    ON_MALFORMED_PACKET = "on_malformed_packet"
    ON_LOGIN_REQUEST = "on_login_request"
    ON_ACTION_QUIT = "on_quit"

    @classmethod
    def _missing_(cls, _: object) -> Any:
        return cls("on_unhandled")
