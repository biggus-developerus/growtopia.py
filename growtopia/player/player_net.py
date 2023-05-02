__all__ = ("PlayerNet",)

from typing import Union

import enet


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

    def send(self, data: Union[str, bytes, enet.Packet]):
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
            self.send_log(data)
        elif isinstance(data, enet.Packet):
            self.peer.send(0, data)
        elif isinstance(data, bytes):
            self.peer.send(0, enet.Packet(data, enet.PACKET_FLAG_RELIABLE))
        else:
            raise TypeError("Invalid data type passed.")

    def send_log(self, text: str):
        """
        Sends a log message to the player.

        Parameters
        ----------
        text: str
            The text to send to the player.
        """
        # TODO: PACKET CLASS!!!!!!!!!!!
        ...
