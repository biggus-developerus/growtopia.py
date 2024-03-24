__all__ = ("ItemSeedInfo",)

from dataclasses import (
    dataclass,
)

from ..utils import Buffer


@dataclass
class ItemSeedInfo:
    base_index: int = 0
    overlay_index: int = 0

    tree_base_index: int = 0
    tree_leaves_index: int = 0

    colour: int = 0
    overlay_colour: int = 0

    @staticmethod
    def from_bytes(data: Buffer) -> "ItemSeedInfo":
        return ItemSeedInfo(
            data.read_int(1),
            data.read_int(1),
            data.read_int(1),
            data.read_int(1),
            data.read_int(4),
            data.read_int(4),
        )

    def to_bytes(self, buffer: Buffer) -> None:
        buffer.write_int(self.base_index, 1)
        buffer.write_int(self.overlay_index, 1)
        buffer.write_int(self.tree_base_index, 1)
        buffer.write_int(self.tree_leaves_index, 1)
        buffer.write_int(self.colour, 4)
        buffer.write_int(self.overlay_colour, 4)
