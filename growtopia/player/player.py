__all__ = ("Player",)

import enet

from .player_net import PlayerNet


class Player(PlayerNet):
    """
    Represents a connected ENet peer.

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
        super().__init__(peer)
