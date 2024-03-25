__all__ = ("Collection",)


from command import (
    Command,
    CommandObject,
)
from net import (
    EventID,
    Listener,
)


class Collection:
    def __new__(cls, *args, **kwargs) -> "Collection":
        instance = super().__new__(cls)

        instance.listeners = {}
        instance.commands = {}

        for value in list[cls.__dict__.values()]:
            if isinstance(value, Listener):
                instance.listeners[value.name] = value
                value._origin = instance

            elif isinstance(value, CommandObject):
                instance.commands[value.name] = value
                value.origin = instance
                value._init_args()

        return instance

    def __init__(self, *args, **kwargs) -> None:
        self.listeners: dict[EventID, Listener]
        self.commands: dict[str, Command]
