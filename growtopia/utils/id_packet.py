__all__ = ("identify_packet",)

from typing import Optional

from ..enums import EventID
from ..protocol import Packet, PacketType


def identify_packet(packet: Packet) -> Optional[EventID]:
    """Identify the type of packet based on its contents."""

    # Common packets are checked for first to avoid unnecessary checks.
    # As of now, the most common packet would be the login packet.
    # In the future, it'll most definitely be a game packet containing state updates.

    if packet.type == PacketType.HELLO:
        return EventID.HELLO

    if packet.type == PacketType.TEXT and "requestedName" in packet.text:
        return EventID.LOGIN_REQUEST

    if packet.type == PacketType.GAME_MESSAGE and packet.game_message.startswith(
        "action"
    ):
        action_type = packet.game_message.split("|")[1].lower()
        return EventID(f"on_{action_type}")

    if packet.type == PacketType.GAME_PACKET:
        return packet.game_packet_type

    return EventID.UNKNOWN
