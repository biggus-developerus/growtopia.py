__all__ = (
    "Packet",
    "StrPacket",
    "TextPacket",
    "MsgPacket",
    "UpdatePacket",
)

from typing import Optional

from growtopia._types import (
    AllData,
    AllStr,
    OptionalPack,
    Pack,
    int8,
    int16,
    int32,
)
from growtopia.utils import (
    Packer,
)

from .enums import (
    PacketType,
    UpdateType,
    UpdateFlags,
)


class Packet(Packer):
    packet_type: Pack[int32]

    def __init__(self, packet_type: PacketType = PacketType.HELLO) -> None:
        self.packet_type: PacketType = packet_type


class StrPacket(Packer):
    packet_type: Pack[int32]
    text: OptionalPack[AllStr]

    def __init__(
        self, packet_type: PacketType = PacketType.TEXT, text: Optional[str] = None
    ) -> None:
        self.packet_type: PacketType = packet_type
        self.text: str = text or ""


class TextPacket(StrPacket):
    def __init__(self, text: Optional[str] = None) -> None:
        super().__init__(PacketType.TEXT, text)


class MsgPacket(StrPacket):
    def __init__(self, text: Optional[None] = None) -> None:
        super().__init__(PacketType.MSG, text)


class UpdatePacket(Packer):
    packet_type: Pack[int32]
    update_type: Pack[int8]
    object_type: Pack[int8]
    count1: Pack[int8]
    count2: Pack[int8]
    net_id: Pack[int32]
    target_net_id: Pack[int32]
    flags: Pack[int32]
    float_: Pack[float]
    int_: Pack[int32]
    vec_x: Pack[float]
    vec_y: Pack[float]
    velo_x: Pack[float]
    velo_y: Pack[float]
    particle_rotation: Pack[float]
    int_x: Pack[int32]
    int_y: Pack[int32]
    extra_data_size: OptionalPack[int32]
    extra_data: OptionalPack[AllData]

    def __init__(
        self,
        *,
        update_type: UpdateType = UpdateType.STATE_UPDATE,
        object_type: int = 0,
        count1: int = 0,
        count2: int = 0,
        net_id: int = -1,
        target_net_id: int = 0,
        flags: UpdateFlags = UpdateFlags.NONE,
        float_: float = 0.0,
        int_: float = 0,
        vec_x: float = 0.0,
        vec_y: float = 0.0,
        velo_x: float = 0.0,
        velo_y: float = 0.0,
        particle_rotation: float = 0.0,
        int_x: int = 0,
        int_y: int = 0,
        extra_data_size: Optional[int] = None,
        extra_data: Optional[bytes] = None,
    ) -> None:
        self.packet_type: PacketType = PacketType.UPDATE
        self.update_type: UpdateType = update_type
        self.object_type: int = object_type
        self.count1: int = count1
        self.count2: int = count2
        self.net_id: int = net_id
        self.target_net_id: int = target_net_id
        self.flags: UpdateFlags = flags
        self.float_: float = float_
        self.int_: float = int_
        self.vec_x: float = vec_x
        self.vec_y: float = vec_y
        self.velo_x: float = velo_x
        self.velo_y: float = velo_y
        self.particle_rotation: float = particle_rotation
        self.int_x: int = int_x
        self.int_y: int = int_y
        self.extra_data_size: int = extra_data_size or None
        self.extra_data: bytes = extra_data or None