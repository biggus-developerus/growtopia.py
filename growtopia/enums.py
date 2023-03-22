__all__ = ("EventID",)

from enum import StrEnum


class EventID(StrEnum):
    UNKNOWN = "on_unknown"

    # ENet events

    CONNECT = "on_connect"
    DISCONNECT = "on_disconnect"
    RECEIVE = "on_receive"

    # Server events
    SERVER_READY = "on_server_ready"

    # Packet events
    LOGIN_REQUEST = "on_login_request"
    QUIT = "on_quit"

    @classmethod
    def _missing_(cls, _):
        return cls.UNKNOWN
