__all__ = ("Dispatcher",)

from asyncio import (
    get_event_loop,
    iscoroutinefunction,
)
from typing import Coroutine

from collection import (
    Collection,
)
from command import (
    CommandObject,
)
from dialog import Dialog
from extension import (
    Extension,
)

from .enums import EventID
from .listener import Listener


class Dispatcher:
    def __init__(self) -> None:
        self.listeners: dict[EventID, Listener] = {}
        self.collection: dict[str, Collection] = {}
        self.extensions: dict[str, Extension] = {}
        self.dialogs: dict[str, Dialog] = {}
        self.commands: dict[str, CommandObject] = {}

    def listener(self, func: Coroutine) -> Listener:
        if not iscoroutinefunction(func):
            raise TypeError("Calllback must be a coroutine function.")

        listener = Listener(func)

        self.add_listeners(listener)

        return listener

    def command(self, func: Coroutine) -> CommandObject:
        if not iscoroutinefunction(func):
            raise TypeError("callback must be a coroutine")

        command = CommandObject(func)

        self.add_commands(command)

        return command

    def add_commands(self, *commands: CommandObject) -> None:
        for command in commands:
            if len(command.aliases) > 0:
                for alias in command.aliases:
                    self.commands[alias] = command

            self.commands[command.name] = command

    def remove_commands(self, *commands: CommandObject) -> None:
        for command in commands:
            if len(command.aliases) > 0:
                for alias in command.aliases:
                    del self.commands[alias]

            del self.commands[command.name]

    def add_listeners(self, *listeners: Listener) -> None:
        for listener in listeners:
            if (
                listener.id == EventID.ON_UNKNOWN
                and listener.callback.__name__ != "on_unknown"
                and not listener._is_origin_dialog
            ):
                raise ValueError(
                    "Callback name must be 'on_unknown' if the ID is 'EventID.ON_UNKNOWN'. This most likely happened because you're trying to register a listener that is not recognised by growtopia.py itself."
                )

            self.listeners[listener.id] = listener

    def remove_listeners(self, *listeners: Listener) -> None:
        for listener in listeners:
            del self.listeners[listener.id]

    def register_dialog(self, dialog: Dialog, *args, **kwargs) -> Dialog:
        dialog = (
            dialog(*args, **kwargs) if isinstance(dialog, type) else dialog
        )  # check if the class is instantiated

        self.dialogs[dialog.name] = dialog

        return Dialog

    def get_dialog(self, name: str) -> Dialog:
        return self.dialogs.get(name, None)

    def unregister_dialog(self, dialog_name: str) -> None:
        del self.dialogs[dialog_name]

    def register_collection(self, col: Collection, *args, **kwargs) -> Collection:
        col = (
            col(*args, **kwargs) if isinstance(col, type) else col
        )  # check if the class is instantiated

        self.collections[col.__class__.__name__] = col

        self.add_listeners(*list(col.listeners.values()))
        self.add_commands(*list(col.commands.values()))

        return col

    def unregister_collection(self, collection_name: str) -> None:
        col = self.collections.get(collection_name, None)

        if not col:
            raise Exception(f"collection {collection_name} is not registered.")

        self.remove_listeners(*list(col.listeners.values()))
        self.remove_commands(*list(col.commands.values()))

    def load_extension(self, module_name: str, package: str = ".", *args, **kwargs) -> None:
        ext = Extension(module_name, package, *args, **kwargs)
        ext.load()

        self.extensions[f"{ext.module.__name__[:-3]}"] = ext

        self.add_listeners(*ext.listeners)
        self.add_commands(*ext.commands)

        for collection in ext.collections:
            self.register_collection(collection, *args, **kwargs)

        for dialog in ext.dialogs:
            self.register_dialog(dialog, *args, **kwargs)

    def unload_extension(self, ext_name: str) -> None:
        ext_name = ext_name if not ext_name.endswith(".py") else ext_name[:-3]
        ext = self.extensions.get(ext_name, None)

        if not ext:
            raise Exception(f"extension {ext_name} is not loaded.")

        for listener in ext.listeners:
            self.remove_listeners(listener)

        for collection in ext.collections:
            self.unregister_collection(collection.__class__.__name__)

        for dialog in ext.dialogs:
            self.unregister_dialog(dialog.name)

        ext.unload()
        self.extensions.pop(ext_name)

    def reload_extension(self, ext_name: str) -> None:
        ext_name = ext_name if not ext_name.endswith(".py") else ext_name[:-3]

        ext = self.extensions.get(ext_name, None)

        if not ext:
            raise Exception(f"extension {ext_name} is not loaded.")

        ext.reload()
        self.load_extension(ext_name, ext.package, *ext._args, **ext._kwargs)

    async def dispatch_event(self, event_id: EventID, *args, **kwargs) -> bool:
        listener = self.listeners.get(event_id, None)

        if listener is None:
            return False

        get_event_loop().create_task(listener(*args, **kwargs))

        return True

    async def dispatch_command(
        self, command_name: str, command_args: list[str], *args, **kwargs
    ) -> bool:
        command = self.commands.get(command_name, None)

        if command is None:
            return False

        c = command(command_args, *args, **kwargs)

        if not c:
            return False

        get_event_loop().create_task(c)

        return True

    async def dispatch_dialog_return(
        self, dialog_name: str, button_name: str, *args, **kwargs
    ) -> bool:
        dialog = self.dialogs.get(dialog_name, None)

        if dialog is None:
            return False

        listener = dialog.listeners.get(button_name, None) or dialog.listeners.get(
            "on_dialog_return", None
        )

        if listener is None:
            return False

        get_event_loop().create_task(listener(*args, **kwargs))

        return True
