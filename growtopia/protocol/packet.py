__all__ = ("Packet",)

from typing import Optional, Union, TYPE_CHECKING

import enet

from ..enums import EventID
from .enums import PacketType

if TYPE_CHECKING:
    from ..player import Player


class Packet:
    """
    A base class for different packet types, such as Text, Game message, Game update, etc.
    This class can also be used to create custom packets.

    Parameters
    ----------
    data: Optional[Union[bytes, enet.Packet]]
        The raw data of the packet.

    Attributes
    ----------
    data: bytes
        The raw data of the packet.
    enet_packet: enet.Packet
        The enet.Packet object created from the raw data.
    type: PacketType
        The type of the packet.
    text: str
        The decoded text that the packet contains. Set by the TextPacket class.
    received_from: Optional[Player]
        The player that sent the packet.
    """

    def __init__(self, data: Optional[Union[bytes, enet.Packet]] = None) -> None:
        if isinstance(data, enet.Packet):
            data = data.data

        self.data: bytes = data or b""
        self.type: PacketType = PacketType(0)

        self.text: str  # set by TextPacket class

        self.received_from: Optional[Player] = None

        if len(self.data) >= 4:
            self.deserialise()

    @property
    def enet_packet(self) -> enet.Packet:
        return enet.Packet(self.data, enet.PACKET_FLAG_RELIABLE)

    @classmethod
    def from_bytes(cls, data: bytes) -> "Packet":
        """
        Create a Packet object from bytes.

        Parameters
        ----------
        data: bytes
            The raw data to create the Packet object from.

        Returns
        -------
        Packet
            The Packet object created from the raw data.
        """

        return cls(data)

    @classmethod
    def get_type(cls, data: bytes) -> PacketType:
        """
        Get the type of the packet.

        Parameters
        ----------
        data: bytes
            The raw data of the packet.

        Returns
        -------
        PacketType
            The type of the packet.
        """

        return PacketType(int.from_bytes(data[:4], "little"))

    def identify(self) -> EventID:
        """
        Identify the packet based on its contents.

        Returns
        -------
        EventID
            The event ID responsible for handling the packet.
        """
        raise NotImplementedError

    def serialise(self) -> bytes:
        """
        Serialise the packet.

        Returns
        -------
        bytes
            The serialised packet.

        Raises
        ------
        NotImplementedError
            This method must be implemented in the child class.
        """

        raise NotImplementedError

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
        NotImplementedError
            This method must be implemented in the child class.
        """

        raise NotImplementedError
