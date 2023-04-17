__all__ = ("_PlayerNetworkFunctions",)

from .protocol import Packet, PacketType


class _PlayerNetworkFunctions:
    def send(self, packet: Packet = None, data: bytes = None) -> None:
        if data is not None:
            packet = Packet.from_bytes(data)

        self.peer.send(0, packet.enet_packet)

    def logon_fail(self) -> None:
        packet = Packet()

        packet.type = PacketType.GAME_MESSAGE
        packet.game_message = "action|logon_fail\n"

        self.send(packet=packet)

    def log(self, text: str) -> None:
        packet = Packet()

        packet.type = PacketType.GAME_MESSAGE
        packet.game_message = f"action|log\nmsg|{text}\n"

        self.send(packet=packet)

    def set_url(self, url: str, label: str) -> None:
        packet = Packet()

        packet.type = PacketType.GAME_MESSAGE
        packet.game_message = f"action|set_url\nurl|{url}\nlabel|{label}\n"

        self.send(packet=packet)
