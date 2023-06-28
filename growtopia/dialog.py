__all__ = ("Dialog",)

from .protocol import GameUpdatePacket, GameUpdatePacketType, GameUpdatePacketFlags, VariantList


class Dialog:
    """
    Represents a text dialog that can be sent to the client.

    Attributes
    ----------
    dialog: str
        The dialog string.
    """

    def __init__(self):
        self.dialog: str = ""

    def add_textbox(self, text: str):
        self.dialog += f"add_textbox|{text}|left|\n"

    def add_smalltext(self, text: str):
        self.dialog += f"add_smalltext|{text}|left|\n"

    def add_spacer_big(self):
        self.dialog += f"add_spacer|big|\n"

    def add_spacer_small(self):
        self.dialog += f"add_spacer|small|\n"

    def add_button_with_icon(self, name: str, text: str, itemid: int):
        self.dialog += f"add_button_with_icon|{name}|{text}|staticBlueFrame|{itemid}|\n"

    def add_picker(self, name: str, text: str, headertext: str):
        self.dialog += f"add_item_picker|{name}|{text}|{headertext}|\n"

    def add_label_with_icon_big(self, text: str, itemid: int):
        self.dialog += f"add_label_with_icon|big|{text}|left|{itemid}|\n"

    def add_label_with_icon_small(self, text: str, itemid: int):
        self.dialog += f"add_label_with_icon|small|{text}|left|{itemid}|\n"

    def add_checkbox(self, name: str, text: str, checked: bool):
        self.dialog += f"add_checkbox|{name}|{text}|{int(checked)}|\n"

    def add_button(self, name: str, text: str):
        self.dialog += f"add_button|{name}|{text}|noflags|0|0|\n"

    def add_ending(self, name: str, cancel: str, accept: str):
        self.dialog += f"end_dialog|{name}|{cancel}|{accept}|\n"

    def allow_quick_exit(self):
        self.dialog += f"add_quick_exit|\n"

    def __str__(self):
        return self.dialog

    def __len__(self):
        return len(self.dialog)

    def encode(self):
        return self.dialog.encode("utf-8")

    @property
    def packet(self) -> GameUpdatePacket:
        packet = GameUpdatePacket()

        packet.update_type = GameUpdatePacketType.CALL_FUNCTION
        packet.set_variant_list(VariantList("OnDialogRequest", self.dialog))

        return packet
