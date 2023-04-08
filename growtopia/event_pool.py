__all__ = ("Pool",)

import asyncio
import inspect
from importlib.machinery import ModuleSpec
from importlib.util import module_from_spec, spec_from_file_location
from types import ModuleType
from typing import Callable

from .collection import Collection
from .enums import EventID
from .listener import Listener


class EventPool:
    def __init__(self) -> None:
        self.__listeners: dict[str, Listener] = {}
        self._event_loop = asyncio.get_event_loop()

    def listener(self, func: Callable) -> Callable:
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("callback must be a coroutine")

        listener = Listener(func)
        self.register_listeners(listener)

        return listener

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

    def _get_module(self, name: str, pck: str = None) -> tuple[ModuleType, ModuleSpec]:
        pck = pck or "."

        return (
            module_from_spec(
                spec := spec_from_file_location(
                    name if not name.endswith(".py") else name[:-3],
                    f"{pck}\{name}",
                )
            ),
            spec,
        )

    def load_extension(self, module_name: str, package: str = None) -> None:
        module, spec = self._get_module(module_name, package)
        spec.loader.exec_module(module)

        for _, value in module.__dict__.items():
            if isinstance(value, Listener):
                self.register_listeners(value)
            elif inspect.isclass(value) and issubclass(value, Collection):
                self.register_collection(value)

    def unload_extension(self, module_name: str, package: str = None) -> None:
        module, spec = self._get_module(module_name, package)
        spec.loader.exec_module(module)

        for _, value in module.__dict__.items():
            if isinstance(value, Listener):
                self.unregister_listeners(value)
            elif inspect.isclass(value) and issubclass(value, Collection):
                self.unregister_collection(value)

    async def _dispatch(self, event_id: EventID, *args, **kwargs) -> None:
        listener = self.__listeners.get(event_id, None)

        if listener:
            self._event_loop.create_task(listener(*args, **kwargs))
