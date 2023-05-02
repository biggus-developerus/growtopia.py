__all__ = ("Dispatcher",)

import asyncio

from typing import Callable

from .enums import EventID
from .listener import Listener


class Dispatcher:
    """
    A base class for classes that dispatch events to listeners.

    Attributes
    ----------
    listeners: dict[EventID, Listener]
        A dictionary that keeps track of all listeners. Event IDs are used as keys and Listener objects are used as values.
    """

    def __init__(self) -> None:
        self.listeners: dict[EventID, Listener]

    def listener(self, func: Callable) -> Callable:
        """
        A decorator that registers a coroutine as a listener.

        Parameters
        ----------
        func: Callable
            The coroutine to register.

        Returns
        -------
        Listener
            The Listener object that was created.

        Raises
        ------
        TypeError
            The coroutine passed in is not a coroutine.
        """
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("callback must be a coroutine")

        listener = Listener(func)
        self.add_listeners(listener)

        return listener

    def add_listeners(self, *listeners: Listener) -> None:
        """
        Adds a listener to the dispatcher.

        Parameters
        ----------
        *listeners: Listener
            The listener(s) to add to the dispatcher.
        """
        for listener in listeners:
            self.listeners[listener.id] = listener
