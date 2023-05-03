__all__ = ("Server",)

from typing import Optional, Union

import enet

from .context import Context
from .dispatcher import Dispatcher
from .enums import EventID
from .event import Event
from .host import Host
from .player import Player


class Server(Host, Dispatcher):
    """
    Represents a Growtopia game server. This class uses the Host class as a base class and extends its functionality.
    This class is also used as a base class for other types of servers, such as ProxyServer and LoginServer.

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
    players_by_name: dict[str, Player]
        A dictionary that has the tank id name (player's username) as the key and the Player object as the value.
    """

    def __init__(
        self,
        address: tuple[str, int],
        **kwargs,
    ) -> None:
        Host.__init__(
            self,
            enet.Address(*address),
            kwargs.get("peer_count", 32),
            kwargs.get("channel_limit", 2),
            kwargs.get("incoming_bandwidth", 0),
            kwargs.get("outgoing_bandwidth", 0),
        )
        Dispatcher.__init__(self)

        self.compress_with_range_coder()
        self.checksum = enet.ENET_CRC32

        self.players: dict[int, Player] = {}
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
        self.players[peer.connectID] = player
        self.players_by_name[player.login_info.tank_id_name] = player

        return player

    def get_player(self, p: Union[enet.Peer, int, str]) -> Optional[Player]:
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
            return self.players.get(p.connectID, None)

        if isinstance(p, int):
            return self.players.get(p, None)

        if isinstance(p, str):
            return self.players_by_name.get(p, None)

        return None

    def remove_player(
        self, p: Union[enet.Peer, int, str], disconnect: bool = False
    ) -> None:
        """
        Removes a player from the players dictionary.

        Parameters
        ----------
        p: Union[enet.Peer, int, str]
            The peer, peer id, or tank id name of the player to remove.
        """
        if player := self.get_player(p):
            self.players.pop(player.peer.connectID, None)
            self.players_by_name.pop(player.login_info.tank_id_name, None)

            if disconnect:
                player.disconnect()

    async def _handle(self, event: Optional[Event]) -> bool:
        """
        Handles a given event.

        Parameters
        ----------
        event: Optional[Event]
            The event to handle. Could be None if the event emitted is on_cleanup.

        Returns
        -------
        bool
            Whether or not the event has been handled by a Listener.
        """

        context = Context()
        context.server = self
        context.event = event

        if event is None:
            return await self.dispatch_event(
                EventID.ON_CLEANUP,
                context,
            )

        enet_event = event.enet_event

        match enet_event.type:
            case enet.EVENT_TYPE_CONNECT:
                context.player = self.new_player(enet_event.peer)
                return await self.dispatch_event(
                    EventID.ON_CONNECT,
                    context,
                )
            case enet.EVENT_TYPE_DISCONNECT:
                context.player = self.get_player(enet_event.peer)
                return await self.dispatch_event(
                    EventID.ON_DISCONNECT,
                    context,
                )
            case enet.EVENT_TYPE_RECEIVE:
                context.player = self.get_player(enet_event.peer)
                return await self.dispatch_event(
                    EventID.ON_RECEIVE,
                    context,
                )
            case _:
                return False
