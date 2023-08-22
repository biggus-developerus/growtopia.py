__all__ = ("Packet",)

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import enet

if TYPE_CHECKING:
    from ..player import Player

from typing import Optional

from ..enums import EventID
from .enums import PacketType


class Packet(ABC):
    """
    This class is a base class that also provides some useful concrete methods.
    """

    def __init__(self, data: Optional[bytearray] = None, *, type_: Optional[PacketType] = None) -> None:
        self.data: bytearray = data or bytearray()

        self._type: PacketType = type_ or PacketType.UNKNOWN
        self._malformed: bool = False

        self.sender: Optional["Player"] = None

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

    @abstractmethod
    def identify(self) -> EventID:
        ...

    @abstractmethod
    def serialise(self) -> bytes:
        ...

    @classmethod
    @abstractmethod
    def from_bytes(cls, data: bytes) -> "Packet":
        ...
