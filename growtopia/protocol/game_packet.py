__all__ = ("GamePacket",)

import struct
from typing import Optional

from ..error_manager import ErrorManager
from ..exceptions import BadPacketLength
from .enums import GamePacketFlags, GamePacketType
from .variant_list import VariantList


class GamePacket:
    def __init__(self) -> None:
        self.game_packet_type: GamePacketType = GamePacketType.UNKNOWN

        self.object_type: int = 0  # uint8
        self.count1: int = 0  # uint8
        self.count2: int = 0  # uint8

        self.net_id: int = -1  # int32
        self.target_net_id: int = 0  # int32

        self.flags: Optional[GamePacketFlags] = 0  # uint32
        self.float: float = 0.0
        self.int: int = 0  # int32

        self.vec_x: float = 0.0
        self.vec_y: float = 0.0
        self.velo_x: float = 0.0
        self.velo_y: float = 0.0

        self.particle_rotation: float = 0.0

        self.int_x: int = 0  # int32
        self.int_y: int = 0  # int32

        self.extra_data_size: int = 0  # uint32
        self.extra_data: bytes = b""  # uint8[]

    def set_variant_list(self, variant_list: VariantList) -> None:
        self.flags = GamePacketFlags.EXTRA_DATA

        self.extra_data = variant_list.serialise()
        self.extra_data_size = len(self.extra_data)

    def get_variant_list(self) -> Optional[VariantList]:
        if self.flags != GamePacketFlags.EXTRA_DATA:
            return None

        return VariantList.from_bytes(self.extra_data)

    def _deserialise_game_packet(self, data: bytes) -> None:
        if len(data) < 52:
            ErrorManager._raise_exception(BadPacketLength(self, ">=52"))
            return

        self.game_packet_type = GamePacketType(int.from_bytes(data[:1], "little"))

        self.object_type = int.from_bytes(data[1:2], "little")
        self.count1 = int.from_bytes(data[2:3], "little")
        self.count2 = int.from_bytes(data[3:4], "little")

        self.net_id = int.from_bytes(data[4:8], "little", signed=True)
        self.target_net_id = int.from_bytes(data[8:12], "little", signed=True)

        self.flags = GamePacketFlags(int.from_bytes(data[12:16], "little"))
        self.float = struct.unpack("f", data[16:20])[0]
        self.int = int.from_bytes(data[20:24], "little", signed=True)

        self.vec_x = struct.unpack("f", data[24:28])[0]
        self.vec_y = struct.unpack("f", data[28:32])[0]

        self.velo_x = struct.unpack("f", data[32:36])[0]
        self.velo_y = struct.unpack("f", data[36:40])[0]

        self.particle_rotation = struct.unpack("f", data[40:44])[0]

        self.int_x = int.from_bytes(data[44:48], "little", signed=True)
        self.int_y = int.from_bytes(data[48:52], "little", signed=True)

        if self.flags == GamePacketFlags.EXTRA_DATA:
            if len(data) < 56:
                ErrorManager._raise_exception(BadPacketLength(self, ">=56"))
                return

            self.extra_data_size = int.from_bytes(data[52:56], "little")
            self.extra_data = data[56:]

    def _serialise_game_packet(self) -> bytes:
        data = b""

        data += self.game_packet_type.value.to_bytes(1, "little")

        data += self.object_type.to_bytes(1, "little")
        data += self.count1.to_bytes(1, "little")
        data += self.count2.to_bytes(1, "little")

        data += self.net_id.to_bytes(4, "little", signed=True)
        data += self.target_net_id.to_bytes(4, "little", signed=True)

        data += self.flags.value.to_bytes(4, "little")
        data += struct.pack("f", self.float)
        data += self.int.to_bytes(4, "little", signed=True)

        data += struct.pack("f", self.vec_x)
        data += struct.pack("f", self.vec_y)
        data += struct.pack("f", self.velo_x)
        data += struct.pack("f", self.velo_y)

        data += struct.pack("f", self.particle_rotation)

        data += self.int_x.to_bytes(4, "little", signed=True)
        data += self.int_y.to_bytes(4, "little", signed=True)

        if self.flags == GamePacketFlags.EXTRA_DATA:
            data += self.extra_data_size.to_bytes(4, "little")
            data += self.extra_data

        return data
