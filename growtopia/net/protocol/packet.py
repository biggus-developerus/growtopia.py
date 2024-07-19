__all__ = (
    "Packet",
    "StrPacket",
    "TextPacket",
    "MessagePacket",
)

from dataclasses import (
    dataclass,
)

from packer import (
    Float,
    Int8,
    Int32,
    OptionalPack,
    Pack,
    packable,
)

from growtopia._types import (
    AllStr,
)

from .enums import PacketType


@packable
@dataclass
class Packet:
    id: Pack[Int32]


@packable
@dataclass
class StrPacket:
    id: Pack[Int32]
    text: OptionalPack[AllStr] = None


@packable
@dataclass
class TextPacket:
    id: Pack[Int32] = PacketType.TEXT
    text: OptionalPack[AllStr] = None


@packable
@dataclass
class MessagePacket:
    id: Pack[Int32] = PacketType.MSG
    text: OptionalPack[AllStr] = None
