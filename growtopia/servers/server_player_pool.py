__all__ = ("ServerPlayerPool",)

import enet

from ..player import Player

# TODO:
# - Find a better way to ID peers. We used to ID peers by their connectID, but for some reason the attribute resets to 0 when the EVENT_TYPE_DISCONNECT event is emitted.


class ServerPlayerPool:
    def __init__(self) -> None:
        self.players: dict[str, Player] = {}  # players by address (host:port) instead of peer connectID (temporary)
        self.players_by_name: dict[str, Player] = {}

    def new_player(self, peer: enet.Peer) -> Player:
        """
        Instantiates a new Player object and adds it to the players dictionary.

        Parameters
        ----------
        peer: enet.Peer
            The peer to create a Player object for.

        Returns
        -------
        Player
            The Player object that was created.
        """
        player = Player(peer)
        self.players[str(peer.address)] = player

        return player

    def get_player(self, p: enet.Peer | int | str) -> Player:
        """
        Retrieves a player from the players dictionary.

        Parameters
        ----------
        p: Union[enet.Peer, int, str]
            The peer, peer id, or tank id name of the player to retrieve.

        Returns
        -------
        Optional[Player]
            The Player object that was retrieved, or None if nothing was found.
        """
        if isinstance(p, enet.Peer):
            return self.players.get(str(p.address), None)

        # if isinstance(p, int):
        #    return self.players.get(p, None)

        if isinstance(p, str):
            return self.players_by_name.get(p, None)

    def remove_player(self, p: enet.Peer | int | str, disconnect: bool = False) -> None:
        """
        Removes a player from the players dictionary.

        Parameters
        ----------
        p: Union[enet.Peer, int, str]
            The peer, peer id, or tank id name of the player to remove.
        """
        if player := self.get_player(p):
            self.players.pop(str(player.peer.address), None)
            self.players_by_name.pop(player.login_info.tankIDName, None)

            if disconnect:
                player.disconnect()
