__all__ = ("GameUpdatePacket",)

import struct
from typing import Optional, Union

import enet

from ..enums import EventID
from ..error_manager import ErrorManager
from ..exceptions import PacketTooSmall, PacketTypeDoesNotMatchContent
from .enums import GameUpdatePacketFlags, GameUpdatePacketType
from .packet import Packet, PacketType
from .variant_list import VariantList

# TODO: Document game update packet fields


class GameUpdatePacket(Packet):
    """
    Represents a game update packet. A packet that contains multiple fields. Uses the Packet class as a base.

    Parameters
    ----------
    data: Optional[Union[bytes, Packet]]
        The raw data of the packet.

    Attributes
    ----------
    data: bytearray
        The raw data of the packet.
    type: PacketType
        The type of the packet.
    """

    def __init__(self, data: Optional[Union[bytearray, bytes, enet.Packet]] = None) -> None:
        super().__init__(data)

        self.type: PacketType = PacketType.GAME_UPDATE

        self.update_type: GameUpdatePacketType = GameUpdatePacketType.UNKNOWN  # uint8

        self.object_type: int = 0  # uint8
        self.count1: int = 0  # uint8
        self.count2: int = 0  # uint8

        self.net_id: int = -1  # int32
        self.target_net_id: int = 0  # int32

        self.flags: GameUpdatePacketFlags = 0  # uint32
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

        self.variant_list: Optional[VariantList] = None

        self.__malformed: bool = False

        if len(self.data) >= 4:
            self.deserialise()

    @property
    def enet_packet(self) -> enet.Packet:
        """
        Create a new enet.Packet object from the raw data.

        Returns
        -------
        enet.Packet
            The enet.Packet object created from the raw data.
        """

        return enet.Packet(self.serialise(), enet.PACKET_FLAG_RELIABLE)

    def set_variant_list(self, variant_list: VariantList) -> None:
        self.flags = GameUpdatePacketFlags.EXTRA_DATA

        self.extra_data = variant_list.serialise()
        self.extra_data_size = len(self.extra_data)

        self.variant_list = variant_list

    def get_variant_list(self) -> Optional[VariantList]:
        if self.flags != GameUpdatePacketFlags.EXTRA_DATA:
            return None

        if self.variant_list:
            return self.variant_list

        self.variant_list = VariantList.from_bytes(self.extra_data)

        return self.variant_list

    def serialise(self) -> bytearray:
        """
        Serialise the packet.

        Returns
        -------
        bytes
            The serialised packet.
        """

        self.data = bytearray()

        self.data += self.type.to_bytes(4, "little")
        self.data += self.update_type.to_bytes(1, "little")

        self.data += self.object_type.to_bytes(1, "little")
        self.data += self.count1.to_bytes(1, "little")
        self.data += self.count2.to_bytes(1, "little")

        self.data += self.net_id.to_bytes(4, "little", signed=True)
        self.data += self.target_net_id.to_bytes(4, "little", signed=True)

        self.data += self.flags.to_bytes(4, "little")
        self.data += struct.pack("f", self.float)
        self.data += self.int.to_bytes(4, "little", signed=True)

        self.data += struct.pack("f", self.vec_x)
        self.data += struct.pack("f", self.vec_y)
        self.data += struct.pack("f", self.velo_x)
        self.data += struct.pack("f", self.velo_y)

        self.data += struct.pack("f", self.particle_rotation)

        self.data += self.int_x.to_bytes(4, "little", signed=True)
        self.data += self.int_y.to_bytes(4, "little", signed=True)

        if self.flags == GameUpdatePacketFlags.EXTRA_DATA:
            self.data += self.extra_data_size.to_bytes(4, "little")
            self.data += self.extra_data

        return self.data

    def deserialise(self, data: Optional[bytes] = None) -> None:
        """
        Deserialise the packet.

        Parameters
        ----------
        data: Optional[bytes]
            The data to deserialise. If this isn't provided,
            the data attribute will be used instead.

        Raises
        ------
        PacketTooSmall
            The packet is too small to be deserialised.

        PacketTypeDoesNotMatchContent
            The packet type does not match the content of the packet.

        Returns
        -------
        None
        """

        data = data or self.data

        if len(data) < 4:
            ErrorManager._raise_exception(PacketTooSmall(self))
            self.__malformed = True
            return

        type = PacketType(int.from_bytes(data[:4], "little"))

        if self.type != PacketType.GAME_UPDATE:
            ErrorManager._raise_exception(PacketTypeDoesNotMatchContent(self))
            self.__malformed = True
            return

        self.type = type

        if len(data) < 52:
            ErrorManager._raise_exception(PacketTooSmall(self, ">=52"))
            self.__malformed = True
            return

        self.update_type = GameUpdatePacketType(int.from_bytes(data[4:5], "little"))

        self.object_type = int.from_bytes(data[5:6], "little")
        self.count1 = int.from_bytes(data[6:7], "little")
        self.count2 = int.from_bytes(data[7:8], "little")

        self.net_id = int.from_bytes(data[8:12], "little", signed=True)
        self.target_net_id = int.from_bytes(data[12:16], "little", signed=True)

        self.flags = GameUpdatePacketFlags(int.from_bytes(data[16:20], "little"))
        self.float = struct.unpack("f", data[20:24])[0]
        self.int = int.from_bytes(data[24:28], "little", signed=True)

        self.vec_x = struct.unpack("f", data[28:32])[0]
        self.vec_y = struct.unpack("f", data[32:36])[0]
        self.velo_x = struct.unpack("f", data[36:40])[0]
        self.velo_y = struct.unpack("f", data[40:44])[0]

        self.particle_rotation = struct.unpack("f", data[44:48])[0]

        self.int_x = int.from_bytes(data[48:52], "little", signed=True)
        self.int_y = int.from_bytes(data[52:56], "little", signed=True)

        if self.flags == GameUpdatePacketFlags.EXTRA_DATA:
            if len(data) < 60:
                ErrorManager._raise_exception(PacketTooSmall(self, ">=60"))
                self.__malformed = True
                return

            self.extra_data = data[60:]
            self.extra_data_size = len(self.extra_data)

    def identify(self) -> EventID:
        """
        Identify the packet based on its contents.

        Returns
        -------
        EventID
            The event ID responsible for handling this packet.
        """
        if self.__malformed:
            return EventID.ON_MALFORMED_PACKET

        if self.update_type == GameUpdatePacketType.CALL_FUNCTION:
            name = self.get_variant_list()[0].value

            if (
                "OnSuperMain" in name
            ):  # I don't like this too... but it's better than having the user write the entire name out 💀💀💀
                return EventID.ON_SUPER_MAIN

            return EventID(name)

        return EventID("on_" + self.update_type.name.lower())
