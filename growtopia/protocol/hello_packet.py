__all__ = ("HelloPacket",)

from ..enums import EventID
from ..error_manager import ErrorManager
from ..exceptions import PacketTooSmall, PacketTypeDoesNotMatchContent
from .enums import PacketType
from .packet import Packet


class HelloPacket(Packet):
    """
    Represents a hello packet. A packet that contains 4 bytes indicating its type (1).

    Parameters
    ----------
    data: Optional[Union[bytes, Packet]]
        The raw data of the packet.

    Attributes
    ----------
    data: bytearray
        The raw data of the packet.
    """

    def __init__(self) -> None:
        super().__init__()
        self._type = PacketType.HELLO

    def serialise(self) -> bytearray:
        """
        Serialise the packet.

        Returns
        -------
        bytes
            The serialised packet.
        """
        self.data = bytearray(int.to_bytes(self._type, 4, "little"))
        return self.data

    def identify(self) -> EventID:
        """
        Identify the packet based on its contents.

        Returns
        -------
        EventID
            The event ID responsible for handling the packet.
        """
        if self._malformed:
            return EventID.ON_MALFORMED_PACKET

        return EventID.ON_HELLO

    @classmethod
    def from_bytes(cls, data: bytes) -> "HelloPacket":
        """
        Deserialises a packet from the bytes given. Returns a HelloPacket object.

        Parameters
        ----------
        data: bytes
            The data to deserialise and make a HelloPacket object out of.

        Raises
        ------
        TypeError:
            If the data wasn't of type bytes.
        PacketTooSmall:
            If the data was too small (<4)
        PacketTypeDoesNotMatchContent:
            If the data did not match the packet's type (HELLO)

        Returns
        -------
        Optional["HelloPacket"]
            Returns a HelloPacket object when the deserialisation is successful, returns None otherwise.
        """
        packet = cls()

        if len(data) < 4:
            ErrorManager._raise_exception(PacketTooSmall(packet, len(data), ">=4"))
            packet._malformed = True
            return

        type_ = PacketType(int.from_bytes(data[:4], "little"))

        if type_ != PacketType.HELLO:
            ErrorManager._raise_exception(PacketTypeDoesNotMatchContent(packet, type_))
            packet._malformed = True
            return

        packet._type = type_
        packet.data = bytearray(data)

        return packet
