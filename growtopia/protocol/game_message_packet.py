__all__ = ("GameMessagePacket",)

from typing import Optional, Union

import enet

from ..enums import EventID
from ..error_manager import ErrorManager
from ..exceptions import PacketTypeDoesNotMatchContent
from .packet import Packet, PacketType


class GameMessagePacket(Packet):
    """
    Represents a game message packet. A packet that contains a game message (basically text). Uses the Packet class as a base.

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
    game_message: str
        The decoded game message found in the packet.
    kvps: dict[str, str]
        Key value pairs from text. (e.g `action|log\nmsg|Hello -> {"action": "log", "msg": "Hello"}`)
    """

    def __init__(
        self, data: Optional[Union[bytearray, bytes, enet.Packet]] = None
    ) -> None:
        super().__init__(data)

        self.type: PacketType = PacketType.GAME_MESSAGE
        self.game_message: str = ""
        self.kvps: dict[str, str] = {}  # key value pairs

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
        self.data += self.game_message.encode("utf-8") + (
            b"\n" if not self.game_message.endswith("\n") else b""
        )

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
        PacketTypeDoesNotMatchContent
            The packet type does not match the content of the packet.

        Returns
        -------
        None
        """

        if data is None:
            data = self.data

        if len(data) >= 4:
            self.type = PacketType(int.from_bytes(data[:4], "little"))

            if self.type != PacketType.GAME_MESSAGE:
                ErrorManager._raise_exception(PacketTypeDoesNotMatchContent(self))

            self.game_message = data[4:-1].decode("utf-8")

            if self.game_message.startswith("action"):
                self.kvps = {
                    kvp[0]: kvp[-1]
                    for kvp in (i.split("|") for i in self.game_message.split("\n"))
                }

    def identify(self) -> EventID:
        """
        Identify the packet based on its contents.

        Returns
        -------
        EventID
            The event ID responsible for handling the packet.
        """
        if self.game_message.startswith("action"):
            return EventID(f"on_{self.kvps['action'].lower()}")
