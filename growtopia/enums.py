__all__ = ("EventID",)

from enum import StrEnum


class EventID(StrEnum):
    # ENet events

    CONNECT = "on_connect"
    DISCONNECT = "on_disconnect"
    RECEIVE = "on_receive"

    # Server events
    SERVER_READY = "on_server_ready"
