__all__ = ("Player",)

import asyncio
from typing import Any, Optional

import enet

from ..inventory import Inventory
from ..item import Item
from .player_avatar import PlayerAvatar
from .player_login_info import PlayerLoginInfo
from .player_net import PlayerNet


class Player(PlayerAvatar, PlayerNet):
    # TODO: Update docstr
    """
    Represents a connected ENet peer.

    Parameters
    ----------
    peer: enet.Peer
        The peer object of the player.
    """

    def __init__(self, peer: enet.Peer) -> None:
        PlayerAvatar.__init__(self)
        PlayerNet.__init__(self)

        self.inventory: Optional[Inventory] = Inventory()

        self.hat: int = 0
        self.chest: int = 0
        self.pants: int = 0
        self.feet: int = 0
        self.face: int = 0
        self.hand: int = 0
        self.back: int = 0
        self.hair: int = 0
        self.neck: int = 0
        self.ances: int = 0
        self.d2: int = 0
        self.d3: int = 0

        self.skin: int = 1348247567

        self._login_info: PlayerLoginInfo = PlayerLoginInfo()
        self._peer: enet.Peer = peer

        self.data: Any = None  # Free to use for storing player data (or anything else really)

    @property
    def login_info(self) -> PlayerLoginInfo:
        """
        Returns the login info of the player.

        Returns
        -------
        PlayerLoginInfo:
            The login info of the player.
        """
        return self._login_info

    @login_info.setter
    def login_info(self, value: PlayerLoginInfo) -> None:
        """
        Sets the login info of the player.

        Parameters
        ----------
        value: PlayerLoginInfo
            The login info to set.
        """
        self._login_info = value

    @property
    def peer(self) -> enet.Peer:
        """
        Returns the peer object of the player.

        Returns
        -------
        enet.Peer:
            The peer object of the player.
        """
        return self._peer

    @peer.setter
    def peer(self, value: enet.Peer) -> None:
        """
        Sets the peer object of the player.

        Parameters
        ----------
        value: enet.Peer
            The peer object to set.
        """
        self._peer = value

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

        self.inventory.add_item(item_id, amount)
        self.send_inventory(self.inventory)

        return True

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

    def get_clothing(self) -> tuple[tuple[int, int, int] | int]:
        return (
            # (self.hat, self.back, self.face),
            # (self.feet, self.neck, self.hand),
            # (self.pants, self.hair, self.chest),
            (self.hair, self.chest, self.pants),
            (self.feet, self.face, self.hand),
            (self.back, self.hat, self.neck),
            self.skin,
            (self.ances, self.d2, self.d3),
        )

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

        return self.world.kill_avatar(self, respawn)

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
