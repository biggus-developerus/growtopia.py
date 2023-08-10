__all__ = ("Player",)

from typing import TYPE_CHECKING, Optional

import enet

from ..inventory import Inventory
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
        self.inventory: Optional[Inventory] = Inventory()

    def play_audio_file(self, file_path: str, delay: int = 0) -> bool:
        """
        Sends a packet that'll make the client play an audio file.

        Parameters
        ----------
        file_path: str
            The path of the file to play.

        delay: int
            The delay in milliseconds.

        Returns
        -------
        bool:
            True if the packet was successfully sent, False otherwise.
        """
        return self._play_sfx(file_path, delay)

    def send_to_world(self, world: Optional["World"]) -> bool:
        """
        Sends the player to a world.

        Parameters
        ----------
        world: World
            The world to send the player to.
        """
        self.world = world or self.world

        if self.world is None:
            return False

        return self.world.add_player(self)

    def send_inventory(self, inventory: Optional[Inventory] = None) -> bool:
        """
        Sends the player their inventory.

        Parameters
        ----------
        inventory: Inventory
            The inventory to send to the player.
        """
        self.inventory = inventory or self.inventory

        if self.inventory is None:
            return False

        return self._send_inventory_state(self.inventory)

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
