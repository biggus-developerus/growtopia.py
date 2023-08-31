__all__ = ("TileExtraDataType",)

from enum import IntEnum


class TileExtraDataType(IntEnum):
    NONE = 0
    DOOR = 1
    SIGN = 2
    LOCK = 3
