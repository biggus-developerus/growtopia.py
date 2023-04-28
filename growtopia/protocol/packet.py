__all__ = ("Packet",)

from typing import Optional

import enet

from .enums import PacketType
from .game_packet import GamePacket


class Packet(GamePacket):
    def __init__(self, data: bytes = None) -> None:
        self._data: bytes = data or b""

        self.type: PacketType = PacketType.UNKNOWN

        self.text: Optional[str] = None
        self.game_message: Optional[str] = None

        super().__init__()

        if data is not None and len(data) > 0:
            self.deserialise()

    def serialise(self) -> bytes:
        data = self.type.value.to_bytes(4, "little")

        if self.type == PacketType.TEXT:
            data += self.text.encode() + b"\n"
        elif self.type == PacketType.GAME_MESSAGE:
            data += self.game_message.encode() + b"\n"
        elif self.type == PacketType.GAME_PACKET:
            data += self._serialise_game_packet()

        return data

    def deserialise(self, data: Optional[bytes] = None) -> None:
        self._data = data or self._data

        if len(self._data) < 4:
            return

        self.type = PacketType(int.from_bytes(self._data[:4], "little"))

        if self.type == PacketType.TEXT:
            self.text = self._data[4:-1].decode()
        elif self.type == PacketType.GAME_MESSAGE:
            self.game_message = self._data[4:-1].decode()
        elif self.type == PacketType.GAME_PACKET:
            self._deserialise_game_packet(self._data[4:])

    def parse_login_packet(self) -> dict[str, str]:
        if self.type != PacketType.TEXT or "requestedName" not in self.text:
            raise ValueError(
                "Packet is not a login packet. Call this method only upon handling the on_login_request event."
            )

        return {kvp[0]: kvp[-1] for i in self.text.split() if (kvp := (i.split("|")))}

    @property
    def enet_packet(self) -> enet.Packet:
        return enet.Packet(self.serialise(), enet.PACKET_FLAG_RELIABLE)

    @classmethod
    def from_bytes(cls, data: bytes) -> "Packet":
        packet = cls()
        packet.deserialise(data)
        return packet

    @classmethod
    def identify_packet(cls, packet: "Packet") -> Optional["EventID"]:
        """
        Identifies the packet handler based on the packet's contents.

        Parameters
        -----------
        packet: `Packet`
            The packet to identify.

        Returns
        --------
        `Optional[EventID]`
            The event id responsible for handling the packet.
        """

        # Common packets are checked for first to avoid unnecessary checks.
        # As of now, the most common packet would be the hello/login packet.
        # In the future, it'll most definitely be a game packet containing state updates.

        if packet.type == PacketType.HELLO:
            return EventID.HELLO

        if packet.type == PacketType.TEXT and "requestedName" in packet.text:
            return EventID.LOGIN_REQUEST

        if (
            packet.type == PacketType.GAME_MESSAGE
            or packet.type == PacketType.TEXT
            and packet.game_message.startswith("action")
        ):
            return EventID(f"on_{packet.game_message.split('|')[1].lower()}")

        if packet.type == PacketType.GAME_PACKET:
            return packet.game_packet_type

        return EventID.UNKNOWN
