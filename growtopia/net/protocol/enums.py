__all__ = ("PacketType",)

from aenum import IntEnum


class PacketType(IntEnum):
    UNKNOWN = 0
    HELLO = 1
    TEXT = 2
    MSG = 3
    UPDATE = 4
