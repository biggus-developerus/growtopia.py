__all__ = ("GameUpdatePacket",)

import struct
from typing import Optional

from ..enums import EventID
from ..error_manager import ErrorManager
from ..exceptions import PacketTooSmall, PacketTypeDoesNotMatchContent
from .enums import GameUpdatePacketFlags, GameUpdatePacketType, PacketType
from .packet import Packet
from .variant_list import VariantList

# TODO: Document game update packet fields


class GameUpdatePacket(Packet):
    """
    Represents a game update packet, a packet that contains multiple fields.

    Kwargs
    ------
    type: Optional[GameUpdatePacketType]
        The update type to instantiate the packet with.
    object_type: Optional[int]:
        The object type to instantiate the packet with.
    count1: int
        The count1 (lost count, could also be used as count for some other stuff) to instantiate the packet with.
    count2: int
        The count2 (gained count, could also be used as count for some other stuff) to instantiate the packet with.
    net_id: int
        The net id to instantiate the packet with.
    target_net_id: int
        The target net id to instantiate the packet with.
    flags: GameUpdatePacketFlags
        The flags to instantiate the packet with.
    float_: float
        The float value to instantiate the packet with.
    int_: int
        The int value to instantiate the packet with.
    vec_x: float
        The vec_x to instantiate the packet with.
    vec_y: float
        The vec_y to instantiate the packet with.
    velo_x: float
        The velo_x to instantiate the packet with.
    velo_y: float
        The velo_y to instantiate the packet with.
    particle_rotation: float
        The particle rotation to instantiate the packet with.
    int_x: int
        The int_x value to instantiate the packet with.
    int_y: int
        The int_y value to instantiate the packet with.
    extra_data_size: int
        The extra data size to instantiate the packet with (no need to be set if you're instantiating the packet with a variant list (below))
    extra_data: bytes
        The extra data to instantiate the packet with (no need to be set if you're instantiating the packet with a variant list (below))
    variant_list: VariantList
        The VariantList object to instantiate the packet with.

    Attributes
    ----------
    data: bytearray
        The raw data of the packet.
    """

    def __init__(
        self,
        *,
        update_type: Optional[GameUpdatePacketType] = GameUpdatePacketType.UNKNOWN,
        object_type: Optional[int] = 0,
        count1: Optional[int] = 0,
        count2: Optional[int] = 0,
        net_id: Optional[int] = -1,
        target_net_id: Optional[int] = 0,
        flags: Optional[GameUpdatePacketFlags] = GameUpdatePacketFlags.UNKNOWN,
        float_: Optional[float] = 0.0,
        int_: Optional[int] = 0,
        vec_x: Optional[float] = 0.0,
        vec_y: Optional[float] = 0.0,
        velo_x: Optional[float] = 0.0,
        velo_y: Optional[float] = 0.0,
        particle_rotation: Optional[float] = 0.0,
        int_x: Optional[int] = 0,
        int_y: Optional[int] = 0,
        extra_data_size: Optional[int] = 0,
        extra_data: bytes = b"",
        variant_list: Optional[VariantList] = None,
    ) -> None:
        super().__init__()

        self._type = PacketType.GAME_UPDATE

        self.update_type: GameUpdatePacketType = update_type

        self.object_type: int = object_type
        self.count1: int = count1
        self.count2: int = count2

        self.net_id: int = net_id
        self.target_net_id: int = target_net_id

        self.flags: GameUpdatePacketFlags = flags
        self.float: float = float_
        self.int: int = int_

        self.vec_x: float = vec_x
        self.vec_y: float = vec_y
        self.velo_x: float = velo_x
        self.velo_y: float = velo_y

        self.particle_rotation: float = particle_rotation

        self.int_x: int = int_x
        self.int_y: int = int_y

        self.extra_data_size: int = extra_data_size
        self.extra_data: bytes = extra_data

        self.variant_list: Optional[VariantList] = variant_list

        if self.variant_list:
            self.set_variant_list(self.variant_list)

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

    def serialise(self) -> bytes:
        """
        Serialise the packet.

        Returns
        -------
        bytes
            The serialised packet.
        """

        self.data = bytearray(self._type.to_bytes(4, "little"))

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

        return bytes(self.data)

    def identify(self) -> EventID:
        """
        Identify the packet based on its contents.

        Returns
        -------
        EventID
            The event ID responsible for handling this packet.
        """
        if self._malformed:
            return EventID.ON_MALFORMED_PACKET

        if self.update_type == GameUpdatePacketType.CALL_FUNCTION and len(self.get_variant_list()) > 0:
            name = self.get_variant_list()[0].value

            if (
                "OnSuperMain" in name
            ):  # I don't like this too... but it's better than having the user write the entire name out 💀💀💀
                return EventID.OnSuperMain

            return EventID.__members__.get(name, EventID.ON_UNHANDLED)

        return EventID("on_" + self.update_type.name.lower())

    @classmethod
    def from_bytes(cls, data: bytes) -> Optional["GameUpdatePacket"]:
        """
        Deserialises a packet from the bytes given. Returns a GameUpdatePacket object.

        Parameters
        ----------
        data: bytes
            The data to deserialise and make a GameUpdatePacket object out of.

        Raises
        ------
        TypeError:
            If the data wasn't of type bytes.
        PacketTooSmall:
            If the data was too small (<4)
        PacketTypeDoesNotMatchContent:
            If the data did not match the packet's type (GAME_UPDATE)

        Returns
        -------
        Optional["GameUpdatePacket"]
            Returns a GameUpdatePacket object when the deserialisation is successful, returns None otherwise.
        """
        update_packet = cls()

        if len(data) < 4:
            ErrorManager._raise_exception(PacketTooSmall(update_packet))
            update_packet._malformed = True
            return

        type = PacketType(int.from_bytes(data[:4], "little"))

        if update_packet._type != PacketType.GAME_UPDATE:
            ErrorManager._raise_exception(PacketTypeDoesNotMatchContent(update_packet))
            update_packet._malformed = True
            return

        update_packet._type = type

        if len(data) < 52:
            ErrorManager._raise_exception(PacketTooSmall(update_packet, ">=52"))
            update_packet._malformed = True
            return

        update_packet.data = bytearray(data)
        update_packet.update_type = GameUpdatePacketType(int.from_bytes(data[4:5], "little"))

        update_packet.object_type = int.from_bytes(data[5:6], "little")
        update_packet.count1 = int.from_bytes(data[6:7], "little")
        update_packet.count2 = int.from_bytes(data[7:8], "little")

        update_packet.net_id = int.from_bytes(data[8:12], "little", signed=True)
        update_packet.target_net_id = int.from_bytes(data[12:16], "little", signed=True)

        update_packet.flags = GameUpdatePacketFlags(int.from_bytes(data[16:20], "little"))
        update_packet.float = struct.unpack("f", data[20:24])[0]
        update_packet.int = int.from_bytes(data[24:28], "little", signed=True)

        update_packet.vec_x = struct.unpack("f", data[28:32])[0]
        update_packet.vec_y = struct.unpack("f", data[32:36])[0]
        update_packet.velo_x = struct.unpack("f", data[36:40])[0]
        update_packet.velo_y = struct.unpack("f", data[40:44])[0]

        update_packet.particle_rotation = struct.unpack("f", data[44:48])[0]

        update_packet.int_x = int.from_bytes(data[48:52], "little", signed=True)
        update_packet.int_y = int.from_bytes(data[52:56], "little", signed=True)

        if update_packet.flags == GameUpdatePacketFlags.EXTRA_DATA:
            if len(data) < 60:
                ErrorManager._raise_exception(PacketTooSmall(update_packet, ">=60"))
                update_packet._malformed = True
                return

            update_packet.extra_data = data[60:]
            update_packet.extra_data_size = len(update_packet.extra_data)

        return update_packet
