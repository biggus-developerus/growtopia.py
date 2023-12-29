from __future__ import annotations

__all__ = ("WorldPlayerPool",)

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from ..player import Player


class WorldPlayerPool(ABC):
    """
    Used to store and manage players in a world.

    Attributes
    ----------
    players: dict[int, Player]
        The players in the world.
    """

    def __init__(self) -> None:
        self.__players: dict[int, "Player"] = {}

    @property
    @abstractmethod
    def next_net_id(self) -> int:
        ...

    @property
    @abstractmethod
    def spawn_pos(self) -> tuple[int, int]:
        ...

    @abstractmethod
    def lambda_broadcast(self, callback: Callable, exclude_net_id: int = -1) -> None:
        ...

    @property
    def players(self) -> dict[int, "Player"]:
        """
        Returns the players in the world.

        Returns
        -------
        dict[int, Player]:
            The players in the world.
        """
        return self.__players

    @players.setter
    def players(self, value: dict[int, "Player"]) -> None:
        """
        Sets the players in the world.

        Parameters
        ----------
        value: dict[int, Player]
            The players to set.
        """
        self.__players = value

    def add_player(self, player: "Player") -> bool:
        """
        Adds a player to the world.

        Parameters
        ----------
        player: Player
            The player to add to the world.

        Returns
        -------
        bool:
            True if the player was added, False otherwise.
        """
        if player.net_id in self.players:
            return False

        if player.world == None:
            player.world = self

        player.net_id = self.next_net_id
        player.pos = self.spawn_pos

        player._send_world(self)
        player._on_spawn(player, True)

        self.lambda_broadcast(lambda p: p._on_spawn(player, False), exclude_net_id=player.net_id)

        for p in self.players.values():
            player._on_spawn(p, False)

        self.next_net_id += 1
        self.players[player.net_id] = player

        return True

    def get_player(self, net_id: int) -> "Player":
        """
        Gets a player by their net id.

        Parameters
        ----------
        net_id: int
            The net id of the player to get.

        Returns
        -------
        Player:
            The player with the net id.
        """
        return self.players.get(net_id, None)

    def remove_player(self, player: "Player") -> bool:
        """
        Removes a player from the world.

        Parameters
        ----------
        player: Player
            The player to remove from the world.

        Returns
        -------
        bool:
            True if the player was removed, False otherwise.
        """
        if player.net_id not in self.players:
            return False

        del self.players[player.net_id]

        self.lambda_broadcast(lambda p: p._on_remove(player), exclude_net_id=player.net_id)

        return True
