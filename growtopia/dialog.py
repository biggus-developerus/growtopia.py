__all__ = (
    "Dialog",
    "DialogElement",
    "DialogReturn",
)

import asyncio
from typing import Any, Callable

from .listener import Listener
from .protocol import GameUpdatePacket, GameUpdatePacketType, TextPacket, VariantList


class DialogElement:
    """
    This class contains static methods that can be used to create dialog elements.
    """

    def textbox(text: str) -> str:
        return f"add_textbox|{text}|left"

    def smalltext(text: str) -> str:
        return f"add_smalltext|{text}|left"

    def spacer_big() -> str:
        return f"add_spacer|big"

    def spacer_small() -> str:
        return f"add_spacer|small"

    def button_with_icon(name: str, text: str, itemid: int) -> str:
        return f"add_button_with_icon|{name}|{text}|staticBlueFrame|{itemid}"

    def picker(name: str, text: str, headertext: str) -> str:
        return f"add_item_picker|{name}|{text}|{headertext}"

    def label_with_icon_big(text: str, itemid: int) -> str:
        return f"add_label_with_icon|big|{text}|left|{itemid}"

    def label_with_icon_small(text: str, itemid: int) -> str:
        return f"add_label_with_icon|small|{text}|left|{itemid}"

    def checkbox(name: str, text: str, checked: bool) -> str:
        return f"add_checkbox|{name}|{text}|{int(checked)}"

    def button(name: str, text: str) -> str:
        return f"add_button|{name}|{text}|noflags|0|0"

    def text_input(name: str, label: str, max_length: int, default_text: str = "") -> str:
        return f"add_text_input|{name}|{label}|{default_text}|{max_length}|"

    def password_input(name: str, label: str, max_length: int, default_text: str = "") -> str:
        return f"add_text_input_password|{name}|{label}|{default_text}|{max_length}|"

    def ending(name: str, cancel: str, accept: str) -> str:
        return f"end_dialog|{name}|{cancel}|{accept}"

    def quick_exit() -> str:
        return f"add_quick_exit"


class Dialog:
    """
    Represents a text dialog that can be sent to the client.

    Parameters
    ----------
    name: str
        The name of the dialog.

    Attributes
    ----------
    name: str
        The name of the dialog.
    dialog: str
        The dialog string.
    elements: list[str]
        The elements that make up the dialog.
    packet: GameUpdatePacket
        The packet that can be sent to the client to display the dialog. (CALL_FUNCTION, OnDialogRequest, self.dialog)
    listeners: dict[str, ButtonListener]
        A dictionary that keeps track of all listeners. Callback names are used as keys and Listener objects are used as values.
    """

    def __new__(cls, *args, **kwargs):
        inst = super().__new__(cls)

        inst.listeners = {}

        for key, value in cls.__dict__.items():
            if isinstance(value, Listener):
                value._belongs_to = inst
                value._is_dialog_listener = True
                inst.listeners[key] = value

        return inst

    def __init__(self, name: str, elements: list[str] = None) -> None:
        self.name: str = name

        self.elements: list[str] = elements or []
        self.listeners: dict[str, Listener]

        self.__has_ending: bool = False

    @classmethod
    def from_string(cls, data: str) -> "Dialog":
        dialog = cls("unknown")

        for element in data.split("\n"):
            if "end_dialog" in element:
                dialog.__has_ending = True
                dialog.name = element.split("|")[1]

            dialog.elements.append(element)

        return dialog

    def add_elements(self, *elements: str) -> None:
        """
        Adds an element to the dialog.

        Parameters
        ----------
        element: str
            The element to add.
        """
        for element in elements:
            if "end_dialog" in element:
                if self.__has_ending:
                    raise ValueError("Dialog already has an ending.")

                self.__has_ending = True
                self.name = element.split("|")[1]

            self.elements.append(element)

    def add_listeners(self, *listeners: Listener) -> None:
        """
        Adds a button listener to the dialog.

        Parameters
        ----------
        listener: Listener
            The button listener to add.
        """
        for listener in listeners:
            self.listeners[listener.name] = listener

    def listener(self, func: Callable) -> Listener:
        """
        Adds a button listener to the dialog.

        Parameters
        ----------
        listener: ButtonListener
            The button listener to add.
        """
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("callback must be a coroutine")

        listener = Listener(func)
        self.add_listeners(listener)

        return listener

    @property
    def dialog(self) -> str:
        if not self.__has_ending:
            self.add_elements(DialogElement.ending(self.name, "Cancel", "Accept"))

        return "|\n".join(self.elements)

    @property
    def packet(self) -> GameUpdatePacket:
        return GameUpdatePacket(
            update_type=GameUpdatePacketType.CALL_FUNCTION,
            variant_list=VariantList(
                "OnDialogRequest",
                self.dialog,
            ),
        )

    def encode(self) -> bytes:
        """
        Encodes the dialog to bytes.
        """
        return self.dialog.encode("utf-8")

    def __str__(self) -> str:
        return self.dialog

    def __len__(self) -> int:
        return len(self.dialog)


class DialogReturn:
    """
    This class is used to structure a dialog that's being returned to the server

    Parameters
    ----------
    dialog: Dialog
        The dialog that's being returned.

    Attributes
    ----------
    dialog: Dialog
        The dialog that's being returned.
    filled_elements: list[str]
        The elements that have been filled.
    packet: TextPacket
        The packet that can be sent to the server to return the dialog.
    """

    # TODO: Add more elements that can be filled (e.g input, checkbox, etc.)

    def __init__(self, dialog: Dialog) -> None:
        self.dialog: Dialog = dialog
        self.filled_elements: list[str] = []

    def add_button_clicked(self, button_name: str) -> None:
        self.filled_elements.append(f"buttonClicked|{button_name}")

    def add_text_input(self, text_input_name: str, value: Any) -> None:
        self.filled_elements.append(f"{text_input_name}|{value}")

    @property
    def packet(self) -> TextPacket:
        return TextPacket(f"action|dialog_return\ndialog_name|{self.dialog.name}\n" + "\n".join(self.filled_elements))
