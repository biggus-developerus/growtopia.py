__all__ = ("identify_packet",)

from typing import Optional

from ..enums import EventID
from ..protocol import Packet, PacketType


def identify_packet(packet: Packet) -> Optional[EventID]:
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
