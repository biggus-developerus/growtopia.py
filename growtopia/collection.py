__all__ = ("Collection",)

from .enums import EventID
from .listener import Listener


class Collection:
    def __new__(cls) -> "Collection":
        inst = super().__new__(cls)
        inst._listeners: dict[EventID, Listener] = {}

        for _, listener in cls.__dict__.items():
            if isinstance(listener, Listener):
                inst._listeners[listener.id] = listener
                listener._belongs_to = inst

        return inst
