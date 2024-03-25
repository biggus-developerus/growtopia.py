__all__ = ("DialogReturn",)


from net import TextPacket

from .dialog import Dialog


class DialogReturn:
    def __init__(self, dialog: Dialog) -> None:
        self.dialog: Dialog = dialog
        self.filled_elements: list[str] = []

    @property
    def packet(self) -> TextPacket:
        return TextPacket(
            f"action|dialog_return\ndialog_name|{self.dialog.name}\n"
            + "\n".join(self.filled_elements)
        )

    def add_button_clicked(self, button_name: str) -> None:
        self.filled_elements.append(f"buttonClicked|{button_name}")

    def add_text_input(self, text_input_name: str, value: any) -> None:
        self.filled_elements.append(f"{text_input_name}|{value}")
