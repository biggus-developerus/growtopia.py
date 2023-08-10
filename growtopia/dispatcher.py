__all__ = ("Dispatcher",)

import asyncio
from typing import Coroutine, Optional

from .collection import Collection
from .dialog import Dialog
from .enums import EventID
from .error_manager import ErrorManager
from .extension import Extension
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
    extensions: dict[str, Extension]
        A dictionary that keeps track of all extensions. Module names are used as keys and Extension objects are used as values.
    dialogs: dict[str, Dialog]
        A dictionary that keeps track of all dialogs. Dialog names are used as keys and Dialog objects are used as values.
    """

    def __init__(self) -> None:
        self.listeners: dict[EventID, Listener] = {}
        self.collections: dict[str, Collection] = {}
        self.extensions: dict[str, Extension] = {}
        self.dialogs: dict[str, Dialog] = {}

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
            if (
                listener.id == EventID.ON_UNKNOWN
                and listener.callback.__name__ != "on_unknown"
                and not listener._is_dialog_listener
            ):
                raise ValueError(
                    "Callback name must be 'on_unknown' if the ID is 'EventID.ON_UNKNOWN'. This most likely happened because you're trying to register a listener that is not recognised by growtopia.py itself."
                )

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

    def register_dialog(self, dialog: Dialog, *args, **kwargs) -> Dialog:
        """
        Registers a dialog.

        Parameters
        ----------
        dialog: Dialog
            The dialog to register.
        """
        dialog = dialog(*args, **kwargs) if isinstance(dialog, type) else dialog  # check if the class is instantiated
        self.dialogs[dialog.name] = dialog

        return Dialog

    def get_dialog(self, name: str) -> Optional[Dialog]:
        """
        Retreives a dialog from the dialogs dictionary.

        Parameters
        ----------
        name: str
            The name of the dialog to retrieve.

        Returns
        -------
        Optional[Dialog]
            The Dialog object that was retrieved, or None if nothing was found.
        """
        return self.dialogs.get(name, None)

    def unregister_dialog(self, dialog_name: str) -> None:
        """
        Unregisters a dialog.

        Parameters
        ----------
        dialog_name: str
            The name of the dialog to unregister.
        """
        del self.dialogs[dialog_name]

    def register_collection(self, col: Collection, *args, **kwargs) -> Collection:
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

        return col

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

    def load_extension(self, module_name: str, package: str = ".", *args, **kwargs) -> None:
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
        ext = Extension(module_name, package, *args, **kwargs)
        ext.load()

        self.extensions[f"{ext.module.__name__[:-3]}"] = ext

        for listener in ext.listeners:
            self.add_listeners(listener)

        for collection in ext.collections:
            self.register_collection(collection, *args, **kwargs)

        for dialog in ext.dialogs:
            self.register_dialog(dialog, *args, **kwargs)

    def unload_extension(self, ext_name: str) -> None:
        """
        Unloads an extension and unregisters its Listeners, Collections, and Dialogs.

        Parameters
        ----------
        ext_name: str
            The name of the extension to unload. This is the name of the module.
        """
        ext_name = ext_name if not ext_name.endswith(".py") else ext_name[:-3]
        ext = self.extensions.get(ext_name, None)

        if not ext:
            ErrorManager._raise_exception(ValueError(f"extension {ext_name} is not loaded."))
            return

        for listener in ext.listeners:
            self.remove_listeners(listener)

        for collection in ext.collections:
            self.unregister_collection(collection.__class__.__name__)

        for dialog in ext.dialogs:
            self.unregister_dialog(dialog.name)

        ext.unload()
        self.extensions.pop(ext_name)

    def reload_extension(self, ext_name: str) -> None:
        """
        Reloads an extension and re-registers its Listeners and Collections.

        Parameters
        ----------
        module_name: str
            The name of the module to reload.
        package: str
            The package to reload the module from.
        """
        ext_name = ext_name if not ext_name.endswith(".py") else ext_name[:-3]
        ext = self.extensions.get(ext_name, None)

        if not ext:
            ErrorManager._raise_exception(ValueError(f"extension {ext_name} is not loaded."))
            return

        ext.reload()
        self.load_extension(ext_name, ext.package, *ext._args_to_pass, **ext._kwargs_to_pass)

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

        asyncio.get_event_loop().create_task(listener(*args, **kwargs))
        return True

    async def dispatch_dialog_return(self, dialog_name: str, button_name: str, *args, **kwargs) -> bool:
        """
        Dispatches a dialog return event to a Listener object.

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

        listener = dialog.listeners.get(button_name, None) or dialog.listeners.get("on_dialog_return", None)

        if listener is None:
            return False

        asyncio.get_event_loop().create_task(listener(*args, **kwargs))
        return True
