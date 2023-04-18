__all__ = ("PlayerPool",)

from typing import Optional

import enet

from .player import Player


class PlayerPool:
    def __init__(self) -> None:
        self.__players: dict[str, Player] = {}

    def new_player(self, peer: enet.Peer) -> Player:
        self.__players[str(peer.address)] = (plyr := Player(peer))
        return plyr

    def get_player(self, address: str) -> Optional[Player]:
        return self.__players.get(address, None)

    def add_player(self, player: Player) -> None:
        self.__players[str(player.address)] = player

    def remove_player(self, player_addr: str) -> Optional[Player]:
        return self.__players.pop(player_addr, None)
