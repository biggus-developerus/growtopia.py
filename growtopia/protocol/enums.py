__all__ = ("PacketType",)

from enum import IntEnum


class PacketType(IntEnum):
    """
    An integer enumeration of all packet types.
    """

    UNKNOWN = 0
    HELLO = 1
    TEXT = 2
    GAME_MESSAGE = 3
    GAME_UPDATE = 4

    @classmethod
    def _missing_(cls, _: int) -> "PacketType":
        return cls(0)
