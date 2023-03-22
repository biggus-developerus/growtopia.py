__all__ = ("Packet",)

from typing import Optional

import enet

from .enums import PacketType
from .game_packet import GamePacket


class Packet(GamePacket):
    def __init__(self) -> None:
        self.data: bytes = b""

        self.type: PacketType = PacketType.UNKNOWN

        self.text: Optional[str] = None
        self.game_message: Optional[str] = None

        super().__init__()

    def serialise(self) -> bytes:
        data = self.type.value.to_bytes(4, "little")

        if self.type == PacketType.TEXT:
            data += self.text.encode() + b"\n"
        elif self.type == PacketType.GAME_MESSAGE:
            data += self.game_message.encode() + b"\n"
        elif self.type == PacketType.GAME_PACKET:
            data += self.serialise_game_packet()

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
            self.deserialise_game_packet(self.data[4:])

    def parse_login_packet(self) -> dict[str, str]:
        if self.type != PacketType.TEXT or "requestedName" not in self.text:
            raise ValueError(
                "Packet is not a login packet. Call this method only upon handling the on_login_request event."
            )

        return {
            kvp[0]: kvp[1]
            for i in self.text.split("\n")
            if len(kvp := (i.split("|"))) == 2
        }

    @property
    def enet_packet(self) -> enet.Packet:
        return enet.Packet(self.serialise(), enet.PACKET_FLAG_RELIABLE)

    @classmethod
    def from_bytes(cls, data: bytes) -> "Packet":
        packet = cls()
        packet.deserialise(data)
        return packet
