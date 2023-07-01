__all__ = (
    "Dialog",
    "DialogElement",
)

import asyncio
from typing import Callable

from .button_listener import ButtonListener
from .protocol import GameUpdatePacket, GameUpdatePacketType, VariantList


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
    button_listeners: dict[str, ButtonListener]
        A dictionary that keeps track of all button listeners. Button names are used as keys and ButtonListener objects are used as values.
    """

    def __new__(cls, *args, **kwargs):
        inst = super().__new__(cls)

        inst.button_listeners = {}

        for key, value in cls.__dict__.items():
            if isinstance(value, ButtonListener):
                value._belongs_to = inst
                inst.button_listeners[key] = value

        return inst

    def __init__(self, name: str, elements: list[str] = None) -> None:
        self.name: str = name

        self.elements: list[str] = elements or []
        self.button_listeners: dict[str, ButtonListener]

        self.__has_ending: bool = False

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

            self.elements.append(element)

    def add_listeners(self, *listeners: ButtonListener) -> None:
        """
        Adds a button listener to the dialog.

        Parameters
        ----------
        listener: ButtonListener
            The button listener to add.
        """
        for listener in listeners:
            self.button_listeners[listener.button_name] = listener

    def listener(self, func: Callable) -> ButtonListener:
        """
        Adds a button listener to the dialog.

        Parameters
        ----------
        listener: ButtonListener
            The button listener to add.
        """
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("callback must be a coroutine")

        listener = ButtonListener(func)
        self.add_listeners(listener)

        return listener

    @property
    def dialog(self) -> str:
        if not self.__has_ending:
            self.add_elements(DialogElement.ending(self.name, "Cancel", "Accept"))

        return "|\n".join(self.elements)

    @property
    def packet(self) -> GameUpdatePacket:
        packet = GameUpdatePacket()

        packet.update_type = GameUpdatePacketType.CALL_FUNCTION
        packet.set_variant_list(VariantList("OnDialogRequest", self.dialog))

        return packet

    def encode(self) -> bytes:
        """
        Encodes the dialog to bytes.
        """
        return self.dialog.encode("utf-8")

    def __str__(self) -> str:
        return self.dialog

    def __len__(self) -> int:
        return len(self.dialog)
