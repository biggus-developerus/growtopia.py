__all__ = ("Dispatcher",)

import asyncio
import inspect
from importlib.machinery import ModuleSpec
from importlib.util import module_from_spec, spec_from_file_location
from types import ModuleType
from typing import Coroutine

from .button_listener import ButtonListener
from .collection import Collection
from .dialog import Dialog
from .enums import EventID
from .error_manager import ErrorManager
from .listener import Listener


class Dispatcher:
    """
    A base class for classes that dispatch events to listeners.

    Attributes
    ----------
    listeners: dict[EventID, Listener]
        A dictionary that keeps track of all listeners. Event IDs are used as keys and Listener objects are used as values.
    collections: dict[str, Collection]
        A dictionary that keeps track of all collections. Collection names are used as keys and Collection objects are used as values.
    extensions: dict[str, ModuleType]
        A dictionary that keeps track of all extensions. Module names are used as keys and ModuleType objects are used as values.
    """

    def __init__(self) -> None:
        self.listeners: dict[EventID, Listener] = {}
        self.collections: dict[str, Collection] = {}
        self.extensions: dict[str, ModuleType] = {}
        self.dialogs: dict[str, Dialog] = {}

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

    def listener(self, func: Coroutine) -> Listener:
        """
        A decorator that registers a coroutine as a listener.

        Parameters
        ----------
        func: Coroutine
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

    def register_dialog(self, dialog: Dialog, *args, **kwargs) -> None:
        """
        Registers a dialog.

        Parameters
        ----------
        dialog: Dialog
            The dialog to register.
        """
        dialog = dialog(*args, **kwargs) if isinstance(dialog, type) else dialog  # check if the class is instantiated
        self.dialogs[dialog.name] = dialog

    def unregister_dialog(self, dialog_name: str) -> None:
        """
        Unregisters a dialog.

        Parameters
        ----------
        dialog_name: str
            The name of the dialog to unregister.
        """
        del self.dialogs[dialog_name]

    def register_collection(self, col: Collection, *args, **kwargs) -> None:
        """
        Registers a collection of Listeners.

        Parameters
        ----------
        col: Collection
            The collection to register.
        *args
            The positional arguments to pass to the collection's constructor.
        **kwargs
            The keyword arguments to pass to the collection's constructor.
        """
        col = col(*args, **kwargs) if isinstance(col, type) else col  # check if the class is instantiated
        self.collections[col.__class__.__name__] = col

        self.add_listeners(*list(col._listeners.values()))

    def unregister_collection(self, collection_name: str) -> None:
        """
        Unregisters a collection of Listeners.

        Parameters
        ----------
        collection_name: str
            The name of the collection to unregister.
        """
        col = self.collections.get(collection_name, None)

        if not col:
            ErrorManager._raise_exception(ValueError(f"collection {collection_name} is not registered."))
            return

        self.remove_listeners(*list(col._listeners.values()))

    def load_extension(self, module_name: str, package: str = None, *args, **kwargs) -> None:
        """
        Loads an extension and registers its Listeners and Collections.

        Parameters
        ----------
        module_name: str
            The name of the module to load.
        package: str
            The package to load the module from.
        *args
            The positional arguments to pass to the constructors of the Collections in the module.
        **kwargs
            The keyword arguments to pass to the constructors of the Collections in the module.
        """
        module, spec = self.__get_module(module_name, package)
        spec.loader.exec_module(module)

        self.extensions[f"{package}.{module.__name__[:-3]}"] = module

        for _, value in module.__dict__.items():
            if isinstance(value, Listener):
                self.add_listeners(value)
            elif inspect.isclass(value) and issubclass(value, Collection):
                self.register_collection(value, *args, **kwargs)
            elif inspect.isclass(value) and issubclass(value, Dialog) and value is not Dialog:
                self.register_dialog(value, *args, **kwargs)

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
        module_name = module_name if not module_name.endswith(".py") else module_name[:-3]
        module = self.extensions.get(f"{package}.{module_name}", None)

        if not module:
            ErrorManager._raise_exception(ValueError(f"extension {module_name} is not loaded."))
            return

        for _, value in module.__dict__.items():
            if isinstance(value, Listener):
                self.remove_listeners(value)
            elif inspect.isclass(value) and issubclass(value, Collection):
                self.unregister_collection(value.__name__)
            elif inspect.isclass(value) and issubclass(value, Dialog):
                self.unregister_dialog(value)

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

    async def dispatch_button_click(self, dialog_name: str, button_name: str, *args, **kwargs) -> bool:
        """
        Dispatches a button click event to a ButtonListener object.

        Parameters
        ----------
        dialog_name: str
            The name of the dialog that the button belongs to.
        button_name: str
            The name of the button to dispatch.
        *args
            The positional arguments to pass to the listener.
        **kwargs
            The keyword arguments to pass to the listener.
        """

        dialog = self.dialogs.get(dialog_name, None)

        if dialog is None:
            return False

        listener = dialog.button_listeners.get(button_name, None)

        if listener is None:
            return False

        await listener(*args, **kwargs)
        return True
