__all__ = ("HelloPacket",)

from typing import Optional, Union

import enet

from ..enums import EventID
from ..error_manager import ErrorManager
from ..exceptions import PacketTooSmall, PacketTypeDoesNotMatchContent
from .packet import Packet, PacketType


class HelloPacket(Packet):
    """
    Represents a hello packet. A packet that contains 4 bytes indicating its type (1). Uses the Packet class as a base.

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

        self.type: PacketType = PacketType.HELLO
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

    def serialise(self) -> bytearray:
        """
        Serialise the packet.

        Returns
        -------
        bytes
            The serialised packet.
        """

        self.data = bytearray(int.to_bytes(self.type, 4, "little"))
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

        if data is None:
            data = self.data

        if len(data) < 4:
            ErrorManager._raise_exception(PacketTooSmall(self))
            self.__malformed = True
            return

        type = PacketType(int.from_bytes(data[:4], "little"))

        if self.type != PacketType.HELLO:
            ErrorManager._raise_exception(PacketTypeDoesNotMatchContent(self))
            self.__malformed = True
            return

        self.type = type

    def identify(self) -> EventID:
        """
        Identify the packet based on its contents.

        Returns
        -------
        EventID
            The event ID responsible for handling the packet.
        """
        if self.__malformed:
            return EventID.ON_MALFORMED_PACKET

        return EventID.ON_HELLO
