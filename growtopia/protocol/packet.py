__all__ = ("Packet",)

from typing import Optional, Union

import enet

from .enums import PacketType


class Packet:
    """
    A base class for different packet types, such as Text, Game message, Game update, etc.
    This class can also be used to create custom packets.

    Attributes
    ----------
    data: bytes
        The raw data of the packet.
    enet_packet: enet.Packet
        The enet.Packet object created from the raw data.
    """

    def __init__(self, data: Union[bytes, enet.Packet]) -> None:
        if isinstance(data, enet.Packet):
            data = data.data

        self.data: bytes = data
        self.packet_type: PacketType = PacketType(1)

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
