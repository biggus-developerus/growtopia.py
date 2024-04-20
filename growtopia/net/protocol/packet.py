__all__ = ("Packet",)

from growtopia._types import (
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
