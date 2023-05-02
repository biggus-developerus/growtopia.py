__all__ = ("EventID",)

from enum import Enum


class EventID(Enum):
    """
    An enumeration of all dispatchable events.
    """

    # ENet events
    ON_CONNECT = "on_connect"
    ON_DISCONNECT = "on_disconnect"
    ON_RECEIVE = "on_receive"
