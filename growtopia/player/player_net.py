__all__ = ("PlayerNet",)

from typing import Optional, Union

import enet

from ..protocol import GameMessagePacket, Packet, TextPacket


class PlayerNet:
    """
    A base class for the Player class. This class is used to handle the networking bit of the Player class.

    Parameters
    ----------
    peer: enet.Peer
        The peer object of the player.

    Attributes
    ----------
    peer: enet.Peer
        The peer object of the player.
    last_packet_sent: None
        The last packet that was sent to the player.
    last_packet_received: None
        The last packet that was received from the player.
    """

    def __init__(self, peer: enet.Peer) -> None:
        self.peer: enet.Peer = peer

        self.last_packet_sent: Optional[Packet] = None
        self.last_packet_received: Optional[Packet] = None

    def _send(
        self, data: bytes = None, flags: int = enet.PACKET_FLAG_RELIABLE, enet_packet: enet.Packet = None
    ) -> None:
        if not data and not enet_packet:
            raise ValueError("No data or packet was passed.")

        self.peer.send(0, enet_packet or enet.Packet(data, flags))

    def send_packet(self, packet: Packet) -> None:
        """
        Sends a packet to the player.

        Parameters
        ----------
        packet: Packet | Any subclass of Packet
            The packet to send to the player.
        """
        if not isinstance(packet, Packet):
            raise TypeError("Invalid packet type passed.")

        self._send(enet_packet=packet.enet_packet)
        self.last_packet_sent = packet

    def send_log(self, text: str) -> None:
        """
        Sends a log message to the player.

        Parameters
        ----------
        text: str
            The text to send to the player.
        """
        packet = GameMessagePacket()
        packet.game_message = "action|log\nmsg|" + text

        self._send(enet_packet=packet.enet_packet)
        self.last_packet_sent = packet

    def disconnect(self, text: Optional[str] = None) -> None:
        """
        Disconnects the player.

        Parameters
        ----------
        text: str
            The text to send to the player before disconnecting them.
        """
        if text:
            self.send_log(text)

        self.peer.disconnect()
