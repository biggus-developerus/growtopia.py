__all__ = ("EventID",)

from enum import Enum


class EventID(Enum):
    """
    An enumeration of all dispatchable events.
    """

    # General events (not related to ENet / Growtopia)
    ON_CLEANUP = "on_cleanup"

    # ENet events
    ON_CONNECT = "on_connect"
    ON_DISCONNECT = "on_disconnect"
    ON_RECEIVE = "on_receive"

    # Packet events
    ON_REQUEST_LOGIN = "on_request_login"
