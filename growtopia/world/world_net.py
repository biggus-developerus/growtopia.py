__all__ = ("WorldNet",)

from typing import Callable, Union

from ..player import Player
from ..protocol import GameMessagePacket, GameUpdatePacket, Packet, TextPacket


class WorldNet:
    def __init__(self) -> None:
        self.players: dict[int, Player]  # players by net id

    def broadcast(
        self, packet: Union[Packet, GameUpdatePacket, GameMessagePacket, TextPacket], exclude_net_id: int = -1
    ) -> None:
        """
        Broadcasts a packet to all players in the world.

        Parameters
        ----------
        packet: Union[Packet, GameUpdatePacket, GameMessagePacket, TextPacket]
            The packet to broadcast.
        """
        for player in self.players.values():
            if player.net_id == exclude_net_id:
                continue

            player.send(packet)

    def lambda_broadcast(self, callback: Callable, exclude_net_id: int = -1) -> None:
        """
        Calls a callback for each player in the world.

        Parameters
        ----------
        callback: Callable(Player)
            The callback to call for each player.
        """
        for player in self.players.values():
            if player.net_id == exclude_net_id:
                continue

            callback(player)
