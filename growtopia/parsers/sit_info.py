__all__ = ("ItemSitInfo",)

from dataclasses import (
    dataclass,
)

from growtopia.utils import (
    Buffer,
)


@dataclass
class ItemSitInfo:
    can_player_sit: bool = False

    sit_player_offset_x: int = 0
    sit_player_offset_y: int = 0

    sit_overlay_x: int = 0
    sit_overlay_y: int = 0

    sit_overlay_offset_x: int = 0
    sit_overlay_offset_y: int = 0

    sit_overlay_texture: str = ""

    @staticmethod
    def from_bytes(data: Buffer) -> "ItemSitInfo":
        return ItemSitInfo(
            bool(data.read_int(1)),
            data.read_int(4),
            data.read_int(4),
            data.read_int(4),
            data.read_int(4),
            data.read_int(4),
            data.read_int(4),
            data.read_str(data.read_int(2)),
        )

    def to_bytes(self, buffer: Buffer) -> None:
        buffer.write_int(int(self.can_player_sit), 1)
        buffer.write_int(self.sit_player_offset_x, 4)
        buffer.write_int(self.sit_player_offset_y, 4)
        buffer.write_int(self.sit_overlay_x, 4)
        buffer.write_int(self.sit_overlay_y, 4)
        buffer.write_int(self.sit_overlay_offset_x, 4)
        buffer.write_int(self.sit_overlay_offset_y, 4)
        buffer.write_int(len(self.sit_overlay_texture.encode()), 2)
        buffer.write_str(self.sit_overlay_texture)
