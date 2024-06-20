__all__ = (
    "Packet",
    "StrPacket",
    "TextPacket",
    "MsgPacket",
    "UpdatePacket",
)

from typing import Optional

import enet

from growtopia._types import (
    AllData,
    AllStr,
    OptionalPack,
    Pack,
    TVariant,
    int8,
    int32,
)
from growtopia.net.protocol.variant import (
    TYPE_TO_OBJ_MAPPING,
)
from growtopia.utils import (
    LOG_LEVEL_ERROR,
    Packer,
    log,
)

from .enums import (
    PacketType,
    UpdateFlags,
    UpdateType,
    VariantType,
)


class Packet(Packer):
    packet_type: Pack[int32]

    def __init__(self, packet_type: PacketType = PacketType.HELLO) -> None:
        self.packet_type: PacketType = packet_type
        self._prepacked_data: Optional[bytearray] = None

    def prepack(self) -> None:
        self._prepacked_data = self.pack()

    def enet_packet(self, flags: int = enet.PACKET_FLAG_RELIABLE) -> enet.Packet:
        if self._prepacked_data:
            return enet.Packet(self._prepacked_data, flags)

        return enet.Packet(self.pack(), flags)


class StrPacket(Packer):
    packet_type: Pack[int32]
    text: OptionalPack[AllStr]

    @staticmethod
    def from_mapping(
        mapping: dict[str, str], packet_type: PacketType = PacketType.MSG
    ) -> "StrPacket":
        return StrPacket(packet_type, "\n".join([f"{k}|{v}\n" for k, v in mapping.items()]))

    def __init__(
        self, packet_type: PacketType = PacketType.TEXT, text: Optional[str] = None
    ) -> None:
        self.packet_type: PacketType = packet_type
        self.text: str = text or ""
        self._prepacked_data: Optional[bytearray] = None

    def prepack(self) -> None:
        self._prepacked_data = self.pack()

    def enet_packet(self, flags: int = enet.PACKET_FLAG_RELIABLE) -> enet.Packet:
        if self._prepacked_data:
            return enet.Packet(self._prepacked_data, flags)

        return enet.Packet(self.pack(), flags)

    def get_mapping(self) -> dict[str, str]:
        if not self.text:
            return {}

        return {kvp[0]: kvp[-1] for i in self.text.split("\n") if (len(kvp := i.split("|")) == 2)}


class TextPacket(StrPacket):
    packet_type: Pack[int32]
    text: OptionalPack[AllStr]

    @staticmethod
    def from_mapping(mapping: dict[str, str]) -> "TextPacket":
        return StrPacket.from_mapping(mapping, PacketType.TEXT)

    def __init__(self, text: Optional[str] = None) -> None:
        super().__init__(PacketType.TEXT, text)


class MsgPacket(StrPacket):
    packet_type: Pack[int32]
    text: OptionalPack[AllStr]

    @staticmethod
    def from_mapping(mapping: dict[str, str]) -> "MsgPacket":
        return StrPacket.from_mapping(mapping, PacketType.MSG)

    def __init__(self, text: Optional[None] = None) -> None:
        super().__init__(PacketType.MSG, text)


# TODO: Add aliases for these awtistic attrs lel
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
        int_: int = 0,
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
        self.int_: int = int_
        self.vec_x: float = vec_x
        self.vec_y: float = vec_y
        self.velo_x: float = velo_x
        self.velo_y: float = velo_y
        self.particle_rotation: float = particle_rotation
        self.int_x: int = int_x
        self.int_y: int = int_y
        self.extra_data_size: Optional[int] = extra_data_size or None
        self.extra_data: Optional[bytes] = extra_data or None
        self._prepacked_data: Optional[bytearray] = None

    def prepack(self) -> None:
        self._prepacked_data = self.pack()

    def enet_packet(self, flags: int = enet.PACKET_FLAG_RELIABLE) -> enet.Packet:
        if self._prepacked_data:
            return enet.Packet(self._prepacked_data, flags)

        return enet.Packet(self.pack(), flags)

    def get_variant_list(self) -> list[TVariant]:
        if not self.flags & UpdateFlags.EXTRA_DATA:
            return []

        offset = 1
        variant_count = self.extra_data[0]
        variants = []

        for i in range(variant_count):
            variant_index = self.extra_data[offset]
            variant_type = VariantType(self.extra_data[offset + 1])

            if variant_index != i:
                log(
                    LOG_LEVEL_ERROR,
                    f"Variant ({variant_type.name}) index doesn't match its position in the list!! (expected index: {i}, got {variant_index})",
                )

                return []

            variant_obj = TYPE_TO_OBJ_MAPPING[variant_type]().from_bytes(self.extra_data[offset:])
            variants.append(variant_obj)

            offset += variant_obj.get_size()

        return variants

    def set_variant_list(self, *variants: TVariant, keep_index: bool = False) -> None:
        self.flags |= UpdateFlags.EXTRA_DATA
        self.extra_data = bytearray(len(variants).to_bytes(1, "little"))

        for i, variant in enumerate(variants):
            if not keep_index:
                variant.index = i

            self.extra_data.extend(variant.pack())

        self.extra_data_size = len(self.extra_data)
