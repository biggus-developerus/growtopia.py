__all__ = ("Packet",)

from typing import Optional

import enet

from .enums import GamePacketType, PacketType


class Packet:
    def __init__(self) -> None:
        self.data: bytes = b""

        self.type: PacketType = PacketType.UNKNOWN

        self.text: Optional[str] = None
        self.game_message: Optional[str] = None

        # game packet fields
        self.game_packet_type: GamePacketType = GamePacketType.UNKNOWN

    def serialise(self) -> bytes:
        data = self.type.value.to_bytes(4, "little")

        if self.type == PacketType.TEXT:
            data += self.text[:-1].encode()
        elif self.type == PacketType.GAME_MESSAGE:
            data += self.game_message[:-1].encode()

        return data

    def deserialise(self, data: Optional[bytes] = None) -> None:
        self.data = data or self.data

        if len(self.data) == 0:
            return

        self.type = PacketType(int.from_bytes(self.data[:4], "little"))

        if self.type == PacketType.TEXT:
            self.text = self.data[4:-1].decode()
        elif self.type == PacketType.GAME_MESSAGE:
            self.game_message = self.data[4:-1].decode()
        elif self.type == PacketType.GAME_PACKET:
            ...

    @property
    def enet_packet(self) -> enet.Packet:
        return enet.Packet(self.serialise(), enet.PACKET_FLAG_RELIABLE)

    @classmethod
    def from_bytes(cls, data: bytes) -> "Packet":
        packet = cls()
        packet.deserialise(data)
        return packet
