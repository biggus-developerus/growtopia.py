__all__ = ("Packet",)

from typing import Optional, Union

import enet

from ..enums import EventID
from .enums import PacketType


class Packet:
    """
    A base class for different packet types, such as Text, Game message, Game update, etc.
    This class can also be used to create custom packets.

    Parameters
    ----------
    data: Optional[Union[bytes, bytearray, enet.Packet]]
        The raw data of the packet.

    Attributes
    ----------
    data: bytearray
        The raw data of the packet.
    enet_packet: enet.Packet
        The enet.Packet object created from the raw data.
    type: PacketType
        The type of the packet.
    text: str
        The text found in the text packet. This attribute is only available in the TextPacket class.
    game_message: str
        The game message found in the game message packet. This attribute is only available in the GameMessagePacket class.
    kvps: dict[str, str]
        Key value pairs from text. (e.g `action|log\nmsg|Hello -> {"action": "log", "msg": "Hello"}`)
    """

    def __init__(
        self, data: Optional[Union[bytes, bytearray, enet.Packet]] = None
    ) -> None:
        if isinstance(data, enet.Packet):
            data = data.data

        self.data: bytearray = bytearray(data) if data is not None else bytearray()
        self.type: PacketType = PacketType(0)

        self.text: str = ""
        self.game_message: str = ""
        self.kvps: dict[str, str] = {}

    @property
    def enet_packet(self) -> enet.Packet:
        """
        Create a new enet.Packet object from the raw data.

        Returns
        -------
        enet.Packet
            The enet.Packet object created from the raw data.
        """
        return enet.Packet(self.data, enet.PACKET_FLAG_RELIABLE)

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
        PacketTypeDoesNotMatchContent
            The packet type does not match the content of the packet.

        Returns
        -------
        None
        """

        raise NotImplementedError
