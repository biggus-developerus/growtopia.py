__all__ = ("TextPacket",)

from typing import Optional

from growtopia.protocol.enums import PacketType

from .str_packet import StrPacket


class TextPacket(StrPacket):
    """
    This class uses StrPacket as base. This class simply sets the packet type to TEXT.

    Parameters
    ----------
    text: Optional[str]
        The text to instantiate the string packet with.

    Attributes
    ----------
    _type: PacketType
        The type of the string packet.
    text: str
        The text that the packet holds.
    action: str
        The action from the text.
    arguments: dict[str, str]
        Action arguments from the text.
    kvps: dict[str, str]
        Key value pairs from the text. (key1|value2\nkey2|value2 -> {"key1": "value1", "key2": "value2"})
    data: bytearray
        The data that the packet holds.
    enet_packet: enet.Packet
        An enet.Packet object instantiated with the data that the packet's holding (flag: PACKET_FLAG_RELIABLE).
    """

    def __init__(self, text: Optional[str] = None) -> None:
        super().__init__(text, type_=PacketType.TEXT)
