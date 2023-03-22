__all__ = ("id_packet",)

from ..enums import EventID
from ..protocol import Packet, PacketType


def id_packet(packet: Packet) -> EventID:
    if packet.type == PacketType.TEXT:
        if "requestedName" in packet.text:
            return EventID.LOGIN_REQUEST
    elif packet.type == PacketType.GAME_MESSAGE:
        ...
    elif packet.type == PacketType.GAME_PACKET:
        return packet.game_packet_type

    return EventID.UNKNOWN
