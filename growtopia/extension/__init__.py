__all__ = ("Extension",)


from importlib.machinery import (
    ModuleSpec,
)
from importlib.util import (
    module_from_spec,
    spec_from_file_location,
)
from inspect import isclass
from types import ModuleType
from typing import Optional

from collection import (
    Collection,
)
from command import (
    CommandObject,
)
from dialog import Dialog
from net import Listener


class Extension:
    def __init__(
        self,
        name: str,
        package: str = ".",
        *args,
        **kwargs,
    ) -> None:
        self.name: str = name
        self.package: str = package

        self.module: Optional[ModuleType] = None
        self.spec: Optional[ModuleSpec] = None

        self.collections: list[Collection] = []
        self.listeners: list[Listener] = []
        self.dialogs: list[Dialog] = []
        self.commands: list[CommandObject] = []

        self._args: tuple[any] = args
        self._kwargs: dict[str, any] = kwargs

    def load(self) -> None:
        (self.module, self.spec) = self._get_module(self.name, self.package)
        self.spec.loader.exec_module(self.module)

        for value in list[self.module.__dict__.values()]:
            if isinstance(value, Listener):
                self.listeners.append(value)
            elif isinstance(value, CommandObject):
                self.commands.append(value)
            elif isclass(value) and issubclass(value, Collection):
                self.collections.append(
                    value(*self._args, **self._kwargs) if isinstance(value, type) else value
                )
            elif isclass(value) and issubclass(value, Dialog) and (value is not Dialog):
                self.dialogs.append(
                    value(*self._args, **self._kwargs) if isinstance(value, type) else value
                )

    def unload(self) -> None:
        self.module = None
        self.spec = None

        self.collections.clear()
        self.listeners.clear()
        self.dialogs.clear()

    def reload(self) -> None:
        self.unload()
        self.load()

    @staticmethod
    def _get_module(name: str, package: str = ".") -> tuple[ModuleType, ModuleSpec]:
        name = name if name.endswith(".py") else name + ".py"

        return (
            module_from_spec(
                spec := spec_from_file_location(
                    name, f"{package}/{name}", submodule_search_locations=[package]
                )
            ),
            spec,
        )
