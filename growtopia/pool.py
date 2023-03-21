__all__ = ("Pool",)

import asyncio
import importlib
import inspect
from typing import Callable

from .collection import Collection
from .enums import EventID
from .listener import Listener


class Pool:
    def __init__(self) -> None:
        self.__listeners: dict[str, Listener] = {}
        self._event_loop = asyncio.get_event_loop()

    def register_listeners(self, *listeners: Listener) -> None:
        for listener in listeners:
            self.__listeners[listener.id] = listener

    def unregister_listeners(self, *listeners: Listener) -> None:
        for listener in listeners:
            self.__listeners.pop(listener.id, None)

    def register_collection(self, collection: Collection) -> None:
        collection = collection()
        self.register_listeners(*list(collection._listeners.values()))

    def unregister_collection(self, collection: Collection) -> None:
        collection = collection()
        self.unregister_listeners(*list(collection._listeners.values()))

    def load_extension(self, path: str) -> None:
        module = importlib.import_module(path)

        for _, value in module.__dict__.items():
            if isinstance(value, Listener):
                self.register_listeners(value)
            elif inspect.isclass(value) and issubclass(value, Collection):
                self.register_collection(value)

    def unload_extension(self, path: str) -> None:
        module = importlib.import_module(path)

        for _, value in module.__dict__.items():
            if isinstance(value, Listener):
                self.unregister_listeners(value)
            elif inspect.isclass(value) and issubclass(value, Collection):
                self.unregister_collection(value)

    def listener(self, func: Callable) -> Callable:
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("callback must be a coroutine")

        listener = Listener(func)
        self.register_listeners(listener)

        return listener

    async def _dispatch(self, event_id: EventID, *args, **kwargs) -> None:
        listener = self.__listeners.get(event_id, None)

        if listener:
            self._event_loop.create_task(listener(*args, **kwargs))
