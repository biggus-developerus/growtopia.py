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
    SERVER_CLEANUP = "on_server_cleanup"  # called when server is shutting down

    # Client events
    CLIENT_READY = "on_client_ready"
    CLIENT_CLEANUP = "on_client_cleanup"  # called when client is shutting down

    # Packet events
    HELLO = "on_hello"
    LOGIN_REQUEST = "on_login_request"
    QUIT = "on_quit"

    @classmethod
    def _missing_(cls, _):
        return cls.UNKNOWN
