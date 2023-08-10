__all__ = ("Player",)

from typing import TYPE_CHECKING, Optional

import enet

from .player_login_info import PlayerLoginInfo
from .player_net import PlayerNet

if TYPE_CHECKING:
    from ..world import World


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
        self.world: Optional[World] = None

    def send_to_world(self, world: "World") -> bool:
        """
        Sends the player to a world.

        Parameters
        ----------
        world: World
            The world to send the player to.
        """
        self.world = world
        return self.world.add_player(self)

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

    @property
    def name(self) -> str:
        """
        Returns the name of the player.

        Returns
        -------
        str:
            The player name.
        """
        return self.login_info.requestedName if self.guest else self.login_info.tankIDName
