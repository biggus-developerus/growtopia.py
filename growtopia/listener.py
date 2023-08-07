__all__ = ("Listener",)

import asyncio
from typing import Callable, Coroutine

from .enums import EventID


class Listener:
    """
    Represents a coroutine function that can be dispatched by an event dispatcher.

    Parameters
    ----------
    callback: Callable
        The coroutine function that will be dispatched.

    Attributes
    ----------
    id: EventID
        The ID of the listener. This attribute can either be set manually or automatically by the function's name.
    name: str
        The name of the listener. This attribute can either be set manually or automatically by the function's name.
    callback: Callable
        The coroutine function that will be dispatched.
    """

    def __init__(self, callback: Callable) -> None:
        if not asyncio.iscoroutinefunction(callback):
            raise TypeError("Callback must be a coroutine function.")

        self.id: EventID = EventID(callback.__name__.lower())

        if self.id == EventID.ON_UNKNOWN and callback.__name__ != "on_unknown":
            raise ValueError(
                "Callback name must be 'on_unknown' if the ID is 'EventID.ON_UNKNOWN'. This most likely happened because you're trying to register a listener that is not recognised by growtopia.py itself."
            )

        self.name: str = callback.__name__
        self.callback: Callable = callback

        self._belongs_to: object = None

    def __call__(self, *args, **kwargs) -> Coroutine:
        if self._belongs_to is not None:
            return self.callback(self._belongs_to, *args, **kwargs)

        return self.callback(*args, **kwargs)
