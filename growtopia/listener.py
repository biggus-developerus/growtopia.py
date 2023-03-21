__all__ = ("Listener",)

import asyncio
from typing import Callable, Coroutine

from .enums import EventID


class Listener:
    def __init__(self, callback: Callable) -> None:
        if not asyncio.iscoroutinefunction(callback):
            raise TypeError("Callback must be a coroutine function.")

        self.id = EventID(callback.__name__.lower())
        self.callback = callback

        self._belongs_to = None

    def __call__(self, *args, **kwargs) -> Coroutine:
        if self._belongs_to is not None:
            return self.callback(self._belongs_to, *args, **kwargs)

        return self.callback(*args, **kwargs)
