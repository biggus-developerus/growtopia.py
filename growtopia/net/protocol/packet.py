__all__ = (
    "Packet",
    "StrPacket",
    "TextPacket",
    "MessagePacket",
    "UpdatePacket",
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
    LengthPrefixedData
)

from .enums import PacketType, UpdateFlags, UpdateType


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

        lines = self.text.split("\n")
        return {key: value for key, value in (line.split("|") for line in lines if "|" in line)}

class TextPacket(StrPacket):
    type: Pack[Int32] = PacketType.TEXT
    text: OptionalPack[AllStr] = None

    @classmethod
    def from_mapping(cls, mapping: dict[str, str]) -> "TextPacket":
        return super().from_mapping(mapping)


class MessagePacket(StrPacket):
    type: Pack[Int32] = PacketType.MSG
    text: OptionalPack[AllStr] = None

    @classmethod
    def from_mapping(cls, mapping: dict[str, str]) -> "TextPacket":
        return super().from_mapping(mapping)

@packable
@dataclass
class UpdatePacket:
    type: Pack[Int32] = PacketType.UPDATE

    update_type: Pack[Int8] = UpdateType.STATE_UPDATE
    object_type: Pack[Int8] = 0
    
    count1: Pack[Int8] = 0 
    count2: Pack[Int8] = 0
    
    net_id: Pack[Int32] = -1
    target_net_id: Pack[Int32] = 0
    
    flags: Pack[Int32] = UpdateFlags.NONE
    
    float_: Pack[Float] = 0.0
    int_: Pack[Int32] = 0
    
    vec_x: Pack[Float] = 0.0
    vec_y: Pack[Float] = 0.0
    
    velo_x: Pack[Float] = 0.0
    velo_y: Pack[Float] = 0.0
    
    particle_rotation: Pack[Float] = 0.0
    
    int_x: Pack[Int32] = 0
    int_y: Pack[Int32] = 0
    
    extra_data: OptionalPack[LengthPrefixedData] = None

