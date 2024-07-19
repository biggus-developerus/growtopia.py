__all__ = (
    "Packet",
    "StrPacket",
    "TextPacket",
    "MessagePacket",
)

from dataclasses import (
    dataclass,
)

from typing import Optional

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
    type: Pack[Int32]


@packable
@dataclass
class StrPacket:
    type: Pack[Int32] = PacketType.MSG
    text: OptionalPack[AllStr] = None

    def __post_init__(self) -> None:
        self.type: PacketType
        self.text: Optional[str]

    @classmethod
    def from_mapping(cls, mapping: dict[str, str]) -> "StrPacket":
        return StrPacket(cls.type, "\n".join([f"{k}|{v}\n" for k, v in mapping.items()]))
    
    def get_mapping(self) -> dict[str, str]:
        if not self.text:
            return {}

        return {kvp[0]: kvp[-1] for i in self.text.split("\n") if (len(kvp := i.split("|")) == 2)}


@packable
@dataclass
class TextPacket(StrPacket):
    type: Pack[Int32] = PacketType.TEXT
    text: OptionalPack[AllStr] = None

    @classmethod
    def from_mapping(cls, mapping: dict[str, str]) -> "TextPacket":
        return super().from_mapping(mapping)


@packable
@dataclass
class MessagePacket(StrPacket):
    type: Pack[Int32] = PacketType.MSG
    text: OptionalPack[AllStr] = None

    @classmethod
    def from_mapping(cls, mapping: dict[str, str]) -> "TextPacket":
        return super().from_mapping(mapping)
