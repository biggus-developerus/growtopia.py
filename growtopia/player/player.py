__all__ = ("Player",)

import enet

from .player_login_info import PlayerLoginInfo
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
    last_packet_sent: Union[StrPacket, GameUpdatePacket]
        The last packet that was sent to the player.
    last_packet_received: Union[StrPacket, GameUpdatePacket]
        The last packet that was received from the player.
    login_info: PlayerLoginInfo
        A PlayerLoginInfo object that contains the data that the player sent when they logged in. (e.g. username, password, etc.)
    """

    def __init__(self, peer: enet.Peer) -> None:
        super().__init__(peer)

        self.login_info: PlayerLoginInfo = PlayerLoginInfo()

    @property
    def guest(self) -> bool:
        """
        Returns whether the player is using a guest account or not.

        Returns
        -------
        bool:
            True if the player is a guest, False otherwise.
        """
        return not self.login_info.tankIDName and not self.login_info.tankIDPass
