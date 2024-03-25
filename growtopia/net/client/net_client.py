__all__ = ("NetClient",)


from typing import (
    Optional,
    Union,
)

from enet import (
    ENET_CRC32,
    PACKET_FLAG_RELIABLE,
    Address,
    Host,
    Packet,
    Peer,
)

from ..protocol import (
    HelloPacket,
    MessagePacket,
    TextPacket,
    UpdatePacket,
)


class NetClient:
    def __init__(
        self,
        address: tuple[str, int],
        peer_count: int = 1,
        channel_limit: int = 2,
        incoming_bandwidth: int = 0,
        outgoing_bandwidth: int = 0,
    ) -> None:
        self.host = Host(None, peer_count, channel_limit, incoming_bandwidth, outgoing_bandwidth)

        self.host.compress_with_range_coder()
        self.host.checksum = ENET_CRC32

        self.address = address
        self.peer: Optional[Peer] = None

    def connect(self) -> Peer:
        new_peer: Peer = self.host.connect(Address(*self.address), 2, 0)

        self.peer = new_peer

        return new_peer

    def disconnect(self, send_quit: bool = True) -> None:
        if self.peer is None:
            return

        if send_quit:
            self.send(packet=TextPacket("action|quit_to_exit\n"))
            self.send(packet=MessagePacket("action|quit\n"))

    def send(
        self,
        packet: Union[HelloPacket, TextPacket, MessagePacket, UpdatePacket],
    ) -> bool:
        if self.peer is None:
            return

        enet_packet = Packet(packet.serialize(), PACKET_FLAG_RELIABLE)

        return True if self.peer.send(0, enet_packet) == 0 else False
