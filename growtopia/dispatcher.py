__all__ = ("Dispatcher",)

import asyncio
import inspect
from importlib.machinery import ModuleSpec
from importlib.util import module_from_spec, spec_from_file_location
from types import ModuleType
from typing import Callable

from .collection import Collection
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
        self.listeners: dict[EventID, Listener] = {}

    @classmethod
    def __get_module(cls, name: str, pck: str = None) -> tuple[ModuleType, ModuleSpec]:
        pck = pck or "."
        name = name if name.endswith(".py") else name + ".py"
        return (
            module_from_spec(
                spec := spec_from_file_location(
                    name,
                    f"{pck}/{name}",
                    submodule_search_locations=[pck],
                )
            ),
            spec,
        )

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

    def remove_listeners(self, *listeners: Listener) -> None:
        """
        Removes a listener from the dispatcher.

        Parameters
        ----------
        *listeners: Listener
            The listener(s) to remove from the dispatcher.
        """
        for listener in listeners:
            del self.listeners[listener.id]

    def register_collection(self, col: Collection) -> None:
        """
        Registers a collection of Listeners.

        Parameters
        ----------
        col: Collection
            The collection to register.
        """
        self.add_listeners(*list(col()._listeners.values()))

    def unregister_collection(self, col: Collection) -> None:
        """
        Unregisters a collection of Listeners.

        Parameters
        ----------
        col: Collection
            The collection to unregister.
        """
        self.remove_listeners(*list(col()._listeners.values()))

    def load_extension(self, module_name: str, package: str = None) -> None:
        """
        Loads an extension and registers its Listeners and Collections.

        Parameters
        ----------
        module_name: str
            The name of the module to load.
        package: str
            The package to load the module from.
        """
        module, spec = self.__get_module(module_name, package)
        spec.loader.exec_module(module)

        for _, value in module.__dict__.items():
            if isinstance(value, Listener):
                self.register_listeners(value)
            elif inspect.isclass(value) and issubclass(value, Collection):
                self.register_collection(value)

    def unload_extension(self, module_name: str, package: str = None) -> None:
        """
        Unloads an extension and unregisters its Listeners and Collections.

        Parameters
        ----------
        module_name: str
            The name of the module to unload.
        package: str
            The package to unload the module from.
        """
        module, spec = self.__get_module(module_name, package)
        spec.loader.exec_module(module)

        for _, value in module.__dict__.items():
            if isinstance(value, Listener):
                self.unregister_listeners(value)
            elif inspect.isclass(value) and issubclass(value, Collection):
                self.unregister_collection(value)

    def reload_extension(self, module_name: str, package: str = None) -> None:
        """
        Reloads an extension and re-registers its Listeners and Collections.

        Parameters
        ----------
        module_name: str
            The name of the module to reload.
        package: str
            The package to reload the module from.
        """
        self.unload_extension(module_name, package)
        self.load_extension(module_name, package)

    async def dispatch_event(self, event_id: EventID, *args, **kwargs) -> bool:
        """
        Dispatches an event to a Listener object.

        Parameters
        ----------
        event_id: EventID
            The event ID to dispatch.
        *args
            The positional arguments to pass to the listener.
        **kwargs
            The keyword arguments to pass to the listener.
        """
        listener = self.listeners.get(event_id, None)

        if listener is None:
            return False

        await listener(*args, **kwargs)
        return True
