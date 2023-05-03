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
    game_message: str
        The decoded game message found in the packet.
    """

    def __init__(self, data: Optional[Union[bytes, enet.Packet]] = None) -> None:
        super().__init__(data)

        self.type: PacketType = PacketType.GAME_MESSAGE
        self.game_message: str = ""

        if len(self.data) >= 4:
            self.deserialise()

    def serialise(self) -> bytes:
        """
        Serialise the packet.

        Returns
        -------
        bytes
            The serialised packet.
        """

        self.data = bytearray(int.to_bytes(self.type, 4, "little"))
        self.data += self.game_message.encode("utf-8") + (
            b"\n" if not self.game_message.endswith(b"\n") else b""
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
        """

        if data is None:
            data = self.data

        if len(data) >= 4:
            self.type = PacketType(int.from_bytes(data[:4], "little"))

            if self.type != PacketType.GAME_MESSAGE:
                ErrorManager._raise_exception(PacketTypeDoesNotMatchContent(self))

            self.game_message = data[4:-1].decode("utf-8")

    def identify(self) -> EventID:
        """
        Identify the packet based on its contents.

        Returns
        -------
        EventID
            The event ID responsible for handling the packet.
        """
        if "requestedName" in self.game_message:
            return EventID.ON_REQUEST_LOGIN
