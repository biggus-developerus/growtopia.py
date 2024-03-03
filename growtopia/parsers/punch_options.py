__all__ = ("ItemPunchOptions", "ItemPunchOption")

from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Any,
    Iterator,
    List,
    Literal,
    Optional,
)


@dataclass
class ItemPunchOption:
    op: str
    args: List[Any] = field(default_factory=list)

    @staticmethod
    def on_punch_start() -> "ItemPunchOption":
        return ItemPunchOption("ONPUNCHSTART")

    @staticmethod
    def update_punch() -> "ItemPunchOption":
        return ItemPunchOption("UPDATEPUNCH")

    @staticmethod
    def op_particle1(particle_id: int) -> "ItemPunchOption":
        return ItemPunchOption("op_particle1", [particle_id])

    @staticmethod
    def op_particle2(particle_id: int) -> "ItemPunchOption":
        return ItemPunchOption("op_particle2", [particle_id])

    @staticmethod
    def particle_position(x: int, y: int) -> "ItemPunchOption":
        return ItemPunchOption("op_params", [x, y])

    @staticmethod
    def punch_audio_file(file_path: str) -> "ItemPunchOption":
        return ItemPunchOption("op_audio", [file_path])

    @staticmethod
    def raise_arm(arm_num: Literal[1, 2], degree: int) -> "ItemPunchOption":
        return ItemPunchOption(f"up_arm{arm_num}", [degree])

    @staticmethod
    def facial_expression(facialex_id: int) -> "ItemPunchOption":
        return ItemPunchOption(f"up_face", [facialex_id])

    @staticmethod
    def spin_arm(arm_num: Literal[1, 2]) -> "ItemPunchOption":
        return ItemPunchOption(f"UP_SPINARM{arm_num}")

    @staticmethod
    def hide_item() -> "ItemPunchOption":
        return ItemPunchOption("RFA_HIDEITEM")

    @staticmethod
    def extend_from_emitter() -> "ItemPunchOption":
        return ItemPunchOption("OP_EXTEND_FROM_EMITTER")

    @staticmethod
    def arm_to_target() -> "ItemPunchOption":
        return ItemPunchOption("OP_ARM2TARGET")

    def __str__(self) -> str:
        args = ":" + ",".join(str(i) for i in self.args) if self.args else ""
        return f"{self.op}{args}"


class ItemPunchOptions:
    def __init__(self, options: Optional[list[ItemPunchOption]] = None) -> None:
        self.options: List[ItemPunchOption] = options or []

    def add_punch_option(self, option: ItemPunchOption) -> None:
        self.options.append(option)

    def to_string(self) -> str:
        return self.__str__()

    @staticmethod
    def from_str(string_opts: str) -> "ItemPunchOptions":
        punch_opts = ItemPunchOptions()

        if not string_opts:
            return punch_opts

        for op in string_opts.split(";"):
            punch_opts.add_punch_option(
                ItemPunchOption(op=(splt := op.split(":"))[0], args=splt[1:])
            )

        return punch_opts

    def __str__(self) -> str:
        return ";".join(str(i) for i in self.options)

    def __iter__(self) -> Iterator[ItemPunchOption]:
        return iter(self.options)
