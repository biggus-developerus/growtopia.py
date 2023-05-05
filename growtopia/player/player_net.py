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

        self.last_packet_sent: None = None
        self.last_packet_received: None = None
        # TODO: PACKET CLASS

    def send(
        self, data: Union[str, set, tuple, list, bytes, enet.Packet, Packet]
    ) -> None:
        """
        Sends data to the player.

        Parameters
        ----------
        data: Union[str, bytes, enet.Packet]
            The data to send to the player. Can be a string, bytes, or an enet.Packet object.

        Raises
        ------
        TypeError
            Invalid data type passed into the function.
        """

        if isinstance(data, str):
            return self.send_log(data)

        # elif isinstance(data, set) or isinstance(data, tuple) or isinstance(data, list):
        #    ...  TODO: Add a new function for sending variant lists

        if isinstance(data, enet.Packet):
            data = data
        elif isinstance(data, (bytes, bytearray)):
            data = enet.Packet(data, enet.PACKET_FLAG_RELIABLE)
        elif isinstance(data, (Packet, TextPacket, GameMessagePacket)):
            data = data.enet_packet
        else:
            raise TypeError("Invalid data type passed.")

        self.peer.send(0, data)

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

        self.send(packet)

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
