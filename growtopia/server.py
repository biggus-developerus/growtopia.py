__all__ = ("Server",)

from typing import Optional, Union

import enet

from .host import Host


class Server(Host):
    """
    Represents a Growtopia server. This class uses the Host class as a base class and extends its functionality.
    This class is used as a base class for other types of servers, such as ProxyServer and LoginServer.

    Parameters
    ----------
    address: tuple[str, int]
        The address to bind the server to.

    Kwarg Parameters
    ----------------
    peer_count: int
        The maximum amount of peers that can connect to the server.
    channel_limit: int
        The maximum amount of channels that can be used.
    incoming_bandwidth: int
        The maximum incoming bandwidth.
    outgoing_bandwidth: int
        The maximum outgoing bandwidth.

    Attributes
    ----------
    players: dict[int, Player]
        A dictionary that has the peer id as the key and the Player object as the value.
    players_by_tankidname: dict[str, Player]
        A dictionary that has the tank id name (player's username) as the key and the Player object as the value.
    """

    def __init__(
        self,
        address: tuple[str, int],
        **kwargs,
    ) -> None:
        super().__init__(
            enet.Address(*address),
            kwargs.get("peer_count", 32),
            kwargs.get("channel_limit", 2),
            kwargs.get("incoming_bandwidth", 0),
            kwargs.get("outgoing_bandwidth", 0),
        )

        # self.__players: dict[int, Player] = {}
        # self.__players_by_tankidname: dict[str, Player] = {}

    # TODO: Make a Player class and change return types

    def new_player(self, peer: enet.Peer) -> ...:
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
        ...

    def get_player(self, p: Union[enet.Peer, int, str]) -> Optional[int]:
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
        ...

    def remove_player(self, p: Union[enet.Peer, int, str]) -> None:
        """
        Removes a player from the players dictionary.

        Parameters
        ----------
        p: Union[enet.Peer, int, str]
            The peer, peer id, or tank id name of the player to remove.
        """
        ...
