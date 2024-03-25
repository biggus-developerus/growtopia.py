__all__ = ("Listener",)


from asyncio import (
    iscoroutinefunction,
)
from typing import (
    Callable,
    Coroutine,
    Optional,
)

from .enums import EventID


class Listener:
    def __init__(self, callback: Callable) -> None:
        if not iscoroutinefunction(callback):
            raise Exception("Callback must be a coroutine function.")

        self.id: EventID = EventID(callback.__name__.lower())

        self.name: str = callback.__name__
        self.callback: Callable = callback

        self._origin: Optional[object] = None
        self._is_origin_dialog: bool = False

    def __call__(self, *args, **kwargs) -> Coroutine:
        if self._origin is not None:
            return self.callback(self._origin, *args, **kwargs)

        return self.callback(*args, **kwargs)
