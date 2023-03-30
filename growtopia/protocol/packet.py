__all__ = ("Packet",)

from typing import Optional

import enet

from .enums import PacketType
from .game_packet import GamePacket


class Packet(GamePacket):
    def __init__(self, data: bytearray = None) -> None:
        self.data: bytearray = data or bytearray()

        self.type: PacketType = PacketType.UNKNOWN

        self.text: Optional[str] = None
        self.game_message: Optional[str] = None

        super().__init__()

        if data is not None and len(data) > 0:
            self.deserialise()

    def serialise(self) -> bytearray:
        data = bytearray(self.type.value.to_bytes(4, "little"))

        if self.type == PacketType.TEXT:
            data.extend(self.text.encode() + b"\n")
        elif self.type == PacketType.GAME_MESSAGE:
            data.extend(self.game_message.encode() + b"\n")
        elif self.type == PacketType.GAME_PACKET:
            data.extend(self.serialise_game_packet())

        return data

    def deserialise(self, data: Optional[bytearray] = None) -> None:
        self.data = (
            data
            if data is not None and data is bytearray
            else bytearray(data)
            if data is not None
            else self.data
        )

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
    def from_bytes(cls, data: bytearray) -> "Packet":
        packet = cls()
        packet.deserialise(data)
        return packet
