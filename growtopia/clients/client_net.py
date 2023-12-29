__all__ = ("ClientNet",)

import enet

from ..protocol import (
    GameMessagePacket,
    GameUpdatePacket,
    HelloPacket,
    StrPacket,
    TextPacket,
)


class ClientNet:
    """
    Helper class that provides net methods for the Client class.

    Parameters
    ----------
    address: tuple[str, int]
        The address that'll be used to connect the peer to. (host:port)

    Kwargs
    ------
    peer_count: int
        The maximum amount of peers that can connect to the server.
    channel_limit: int
        The maximum amount of channels that can be used.
    incoming_bandwidth: int
        The maximum incoming bandwidth.
    outgoing_bandwidth: int
        The maximum outgoing bandwidth.
    """

    def __init__(
        self,
        address: tuple[str, int],
        **kwargs,
    ) -> None:
        self._host = enet.Host(
            None,
            kwargs.get("peer_count", 1),
            kwargs.get("channel_limit", 2),
            kwargs.get("incoming_bandwidth", 0),
            kwargs.get("outgoing_bandwidth", 0),
        )

        self._host.compress_with_range_coder()
        self._host.checksum = enet.ENET_CRC32

        self._address: tuple[str, int] = address
        self._peer: enet.Peer = None

    def connect(self) -> enet.Peer:
        """
        Connects to the server.

        Returns
        -------
        enet.Peer
            The peer that was used to connect to the server.
        """
        self._peer = self._host.connect(enet.Address(*self._address), 2, 0)
        return self._peer

    def disconnect(self, send_quit: bool = True) -> None:
        """
        Disconnects from the server.

        Parameters
        ----------
        send_quit: bool
            Whether to send the quit packet to the server.

        Returns
        -------
        None
        """
        if self._peer is None:
            return

        if send_quit:
            self.send(packet=TextPacket("action|quit_to_exit\n"))
            self.send(packet=GameMessagePacket("action|quit\n"))

            self.running = False

        self._peer.disconnect_now(0)
        self._peer = None

    def send(self, packet: StrPacket | GameUpdatePacket | HelloPacket) -> bool:
        """
        Sends a packet to the host.

        Parameters
        ----------
        packet: Union[StrPacket, GameUpdatePacket, HelloPacket]
            The packet to send to the host.

        Returns
        -------
        bool:
            True if the packet was successfully sent, False otherwise.
        """
        if self._peer is not None:
            return True if self._peer.send(0, packet.enet_packet) == 0 else False
