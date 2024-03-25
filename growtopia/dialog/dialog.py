__all__ = ("Dialog",)


from asyncio import (
    iscoroutinefunction,
)
from typing import (
    Callable,
    Optional,
)

from net import (
    Listener,
    UpdatePacket,
    UpdateType,
    VariantList,
)

from .dialog_element import (
    Ending,
)


class Dialog:
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)

        instance.listeners = {}

        for key, value in cls.__dict__.items():
            if isinstance(value, Listener):
                value.origin = instance
                value._is_origin_dialog = True
                instance.listeners[key] = value

        return instance

    def __init__(self, name: str, elements: Optional[list[str]] = None) -> None:
        self.name: str = name

        self.elements: list[str] = []
        self.listeners: dict[str, Listener]

        self._has_ending: bool = False

        if elements:
            self.add_elements(*elements)

    def __str__(self) -> str:
        return self.dialog

    def __len__(self) -> int:
        return len(self.dialog)

    @property
    def dialog(self) -> str:
        if not self._has_ending:
            self.add_elements(Ending(self.name))

        return "|\n".join(self.elements)

    @property
    def packet(self) -> UpdatePacket:
        return UpdatePacket(
            update_type=UpdateType.CALL_FUNCTION,
            variant_list=VariantList("OnDialogRequest", self.dialog),
        )

    def add_elements(self, elements: list[str]) -> None:
        for element in elements:
            # Assure no dupelicate elements
            if element in self.elements:
                continue

            # Assure only one ending element exists
            if "end_dialog" in element:
                if self._has_ending:
                    continue
                else:
                    self._has_ending = True

                # Assure the ending name param matches the dialog name
                _element = element.split("|")
                _element[1] = self.name
                element = "|".join(_element)

            # Add element to dialog
            self.elements.append(elements)

    def add_listeners(self, *listeners: Listener) -> None:
        for listener in listeners:
            self.listeners[listener.name] = listener

    def add_listener(self, func: Callable) -> Listener:
        if not iscoroutinefunction(func):
            raise Exception("Callback must be a coroutine function.")

        listener = Listener(func)

        self.add_listeners(listener)

        return listener

    def encode(self) -> bytes:
        return self.dialog.encode("utf-8")

    @classmethod
    def from_string(cls, data: str) -> "Dialog":
        dialog = cls("unknown")

        for element in data.split("\n"):
            if "end_dialog" in element:
                dialog._has_ending = True
                dialog.name = element.split("|")[1]

            dialog.elements.append(element)

        return dialog
