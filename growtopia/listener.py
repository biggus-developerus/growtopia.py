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

        self.name: str = callback.__name__
        self.callback: Callable = callback

        self._belongs_to: object = None
        self._is_dialog_listener: bool = False

    def __call__(self, *args, **kwargs) -> Coroutine:
        if self._belongs_to is not None:
            return self.callback(self._belongs_to, *args, **kwargs)

        return self.callback(*args, **kwargs)
