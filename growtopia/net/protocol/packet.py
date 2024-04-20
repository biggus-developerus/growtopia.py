__all__ = (
    "Packet",
    "StrPacket",
    "TextPacket",
    "MsgPacket",
)

from typing import Optional

from growtopia._types import (
    AllStr,
    OptionalPack,
    Pack,
    int32,
)
from growtopia.utils import (
    Packer,
)

from .enums import PacketType


class Packet(Packer):
    packet_type: Pack[int32]

    def __init__(self, packet_type: int = PacketType.HELLO) -> None:
        self.packet_type: int = packet_type


class StrPacket(Packer):
    packet_type: Pack[int32]
    text: OptionalPack[AllStr]

    def __init__(self, packet_type: int = PacketType.TEXT, text: Optional[str] = None) -> None:
        self.packet_type: int = packet_type
        self.text: str = text or ""


class TextPacket(StrPacket):
    def __init__(self, text: Optional[str] = None) -> None:
        super().__init__(PacketType.TEXT, text)


class MsgPacket(StrPacket):
    def __init__(self, text: Optional[None] = None) -> None:
        super().__init__(PacketType.MSG, text)
