__all__ = ("Player",)

import enet

from .protocol import Packet


class Player:
    def __init__(self, peer: enet.Peer) -> None:
        self.peer: enet.Peer = peer
        self.address: enet.Address = peer.address

    def send(self, packet: Packet = None, data: bytes = None) -> None:
        if data is not None:
            packet = Packet.from_bytes(data)

        self.peer.send(0, packet.enet_packet)
