__all__ = ("Extension",)

import inspect
from importlib.machinery import ModuleSpec
from importlib.util import module_from_spec, spec_from_file_location
from types import ModuleType

from .collection import Collection
from .dialog import Dialog
from .listener import Listener


class Extension:
    def __init__(self, name: str, package: str = ".", *args, **kwargs) -> None:
        self.name: str = name
        self.package: str = package

        self.module: ModuleType = None
        self.spec: ModuleSpec = None

        self.collections: list[Collection] = []
        self.listeners: list[Listener] = []
        self.dialogs: list[Dialog] = []

        self._args_to_pass: tuple = args
        self._kwargs_to_pass: dict = kwargs

    def load(self) -> None:
        """
        Loads the extension.
        """
        self.module, self.spec = self._get_module(self.name, self.package)
        self.spec.loader.exec_module(self.module)

        for _, value in self.module.__dict__.items():
            if isinstance(value, Listener):
                self.listeners.append(value)
            elif inspect.isclass(value) and issubclass(value, Collection):
                self.collections.append(
                    value(*self._args_to_pass, **self._kwargs_to_pass) if isinstance(value, type) else value
                )
            elif inspect.isclass(value) and issubclass(value, Dialog) and value is not Dialog:
                self.dialogs.append(
                    value(*self._args_to_pass, **self._kwargs_to_pass) if isinstance(value, type) else value
                )

    def unload(self) -> None:
        """
        Unloads the extension.
        """
        self.module = None
        self.spec = None

        self.collections.clear()
        self.listeners.clear()
        self.dialogs.clear()

    def reload(self) -> None:
        """
        Reloads the extension.
        """
        self.unload()
        self.load()

    @staticmethod
    def _get_module(name: str, pck: str = ".") -> tuple[ModuleType, ModuleSpec]:
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
