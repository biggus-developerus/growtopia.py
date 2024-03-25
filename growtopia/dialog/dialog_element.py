__all__ = (
    "QuickExit",
    "Textbox",
    "Text",
    "Button",
    "Picker",
    "Checkbox",
    "Ending",
    "SpacerSize",
    "Spacer",
    "IconSize",
    "LabelWithIcon",
    "Input",
    "EmbedData",
)


from aenum import StrEnum


def QuickExit() -> str:
    return "add_quick_exit"


def Textbox(text: str) -> str:
    return f"add_textbox|{text}|left"


def Text(text: str) -> str:
    return f"add_smalltext|{text}|left"


def Button(name: str, text: str) -> str:
    return f"add_button|{name}|{text}|noflags|0|0"


def Picker(name: str, text: str, header: str) -> str:
    return f"add_item_picekr|{name}|{text}|{header}"


def Checkbox(name: str, text: str, checked: bool = False) -> str:
    return f"add_checkbox|{name}|{text}|{int(checked)}"


def Ending(name: str, cancel_text: str = "Cancel", accept_text: str = "Accept") -> str:
    return f"end_dialog|{name}|{cancel_text}|{accept_text}"


class SpacerSize(StrEnum):
    SMALL = "small"
    BIG = "big"


def Spacer(size: SpacerSize = SpacerSize.SMALL) -> str:
    return f"add_spacer|{size}"


class IconSize(StrEnum):
    SMALL = "small"
    BIG = "big"


def LabelWithIcon(text: str, item_id: int, icon_size: IconSize = IconSize.SMALL) -> str:
    return f"add_label_with_icon|{icon_size}|{text}|{item_id}"


def Input(
    name: str, label: str, max_length: int, default_text: str = "", password: bool = False
) -> str:
    return (
        "add_text_input" + "_password"
        if password
        else "" + f"|{name}|{label}|{default_text}|{max_length}"
    )


def EmbedData(data: dict[str, str]) -> str:
    return "\n".join([f"embed_data|{key}|{value}" for key, value in data.items()])
