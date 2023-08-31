__all__ = ("Player",)

import asyncio
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
        self.pos: tuple[int, int] = ()

        # states

        self.frozen: bool = False
        self.invisible: bool = False
        self.moderator: bool = False
        self.super_moderator: bool = False

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

    def add_inventory_item(self, item_id: int, amount: int = 1) -> bool:
        """
        Adds an item to the player's inventory.

        Parameters
        ----------
        item_id: int
            The item ID to add.

        amount: int
            The amount of the item to add.

        Returns
        -------
        bool:
            True if the item was successfully added, False otherwise.
        """
        if self.inventory is None:
            return False

        return self.inventory.add_item(item_id, amount)

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

    def set_pos(self, x: int, y: int, player: Optional["Player"] = None) -> bool:
        """
        Sets the position of a player.

        Parameters
        ----------
        x: int
            The x pos of where the player will be.
        y: int
            The y pos of where the player will be.
        player: Optional["Player"]
            The player to set the position of.

        Returns
        -------
        bool:
            True if the player had their position updated, False otherwise.
        """
        return self.on_set_pos(x, y, player)

    def kill(self, respawn: bool = True) -> bool:
        """
        Kills the player.
        Simply calls World.kill_player, which sends a packet that'll show the respawn animation.

        Parameters
        ----------
        respawn: bool
            Whether the player should return to the world's spawn position or not.

        Returns
        -------
        bool:
            True if the player was killed, False otherwise.
        """
        if self.world is None:
            return False

        return self.world.kill_player(self, respawn)

    async def freeze(self, duration: float) -> None:
        """
        Freezes the player for a certain amount of time.

        Parameters
        ----------
        duration: float
            The duration in seconds to freeze the player for.

        Returns
        -------
        None
        """
        self.frozen = True
        self.on_set_freeze_state(self.frozen)

        await asyncio.sleep(duration)

        self.frozen = False
        self.on_set_freeze_state(self.frozen)

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
