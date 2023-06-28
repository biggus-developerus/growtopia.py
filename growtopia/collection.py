__all__ = ("Collection",)

from .enums import EventID
from .listener import Listener


class Collection:
    """
    This class is used to store Listener objects. This class is used as a base class for other classes that store Listener objects.

    Attributes
    ----------
    _listeners: dict[EventID, Listener]
        A dictionary that keeps track of all listeners. Event IDs are used as keys and Listener objects are used as values.
    """

    def __new__(cls, *args, **kwargs) -> "Collection":
        inst = super().__new__(cls)
        inst._listeners = {}

        for _, listener in cls.__dict__.items():
            if isinstance(listener, Listener):
                inst._listeners[listener.id] = listener
                listener._belongs_to = inst

        return inst

    def __init__(self, *args, **kwargs) -> None:
        self._listeners: dict[EventID, Listener]
