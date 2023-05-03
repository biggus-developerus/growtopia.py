__all__ = ("TextPacket",)

from typing import Union
from .packet import Packet, PacketType

from typing import Union, Optional

# TODO: Whilst deserialising the packet, we **must** ensure that the packet type matches the packet type of the class (text).
# We could do that by raising an Exception


class TextPacket(Packet):
    """
    Represents a text packet. A packet that contains text. Uses the Packet class as a base.

    Parameters
    ----------
    data: Union[bytes, Packet]
        The raw data of the packet.

    Attributes
    ----------
    text: str
        The text of the packet.

    """

    def __init__(self, data: Union[bytes, Packet]) -> None:
        super().__init__(data)

        self.type: PacketType = PacketType.TEXT
        self.text: str = ""

    def set_text(self, text: str) -> None:
        """
        Sets the text of the packet.

        Parameters
        ----------
        text: str
            The text to set the packet's text to.
        """
        self.text = text + "\n"

    def append_text(self, text: str) -> None:
        """
        Appends text to the packet.

        Parameters
        ----------
        text: str
            The text to append to the packet.
        """

        self.text += text[:-1] + "\n"

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

        self.data = bytearray(int.to_bytes(self.type, 4, "little"))
        self.data += self.text[:-1].encode("utf-8")

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
        NotImplementedError
            This method must be implemented in the child class.
        """

        if data is None:
            data = self.data

        if len(data) >= 4:
            self.type = PacketType(int.from_bytes(data[:4], "little"))
            self.text = data[4:-1].decode("utf-8")
