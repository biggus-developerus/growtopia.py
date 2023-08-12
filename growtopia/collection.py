__all__ = ("Collection",)

from .command import Command
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
        inst._commands = {}

        for _, value in cls.__dict__.items():
            if isinstance(value, Listener):
                inst._listeners[value.id] = value
                value._belongs_to = inst

            elif isinstance(value, Command):
                inst._commands[value.name] = value
                value._belongs_to = inst
                value._init_args()

        return inst

    def __init__(self, *args, **kwargs) -> None:
        self._listeners: dict[EventID, Listener]
        self._commands: dict[str, Command]
