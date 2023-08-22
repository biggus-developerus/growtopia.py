__all__ = ("WorldPlayerPool",)

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..player import Player

from .world_net import WorldNet


class WorldPlayerPool(WorldNet):
    """
    Used to store and manage players in a world.

    Attributes
    ----------
    players: dict[int, Player]
        The players in the world.
    """

    def __init__(self) -> None:
        super().__init__()

        self.players: dict[int, "Player"] = {}
        self.__net_id: int = 0

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

        player.net_id = self.__net_id
        self.players[player.net_id] = player

        player._send_world(self)
        player.on_spawn(500, 500)

        self.lambda_broadcast(lambda p: p.on_spawn(500, 500, player), exclude_net_id=player.net_id)

        for p in self.players.values():
            if p.net_id == player.net_id:
                continue

            player.on_spawn(500, 500, p)

        self.__net_id += 1

        return True

    def get_player(self, net_id: int) -> Optional["Player"]:
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
