__all__ = ("LoginServer",)

from typing import Optional

import enet

from .context import Context
from .enums import EventID
from .event import Event
from .protocol import GameMessagePacket, Packet, PacketType, TextPacket
from .server import Server


class LoginServer(Server):
    """
    Represents a Growtopia login server. This class uses the Server class as a base class and extends its functionality.
    This type of server is specifically used to handle login requests. You may only handle a couple of events with this server,
    like ON_CONNECT, ON_DISCONNECT, ON_RECEIVE, and ON_LOGIN_REQUEST (and stuff like refresh_item_data and refresh_player_tribute).

    A login server is used to handle incoming login requests, hence the name 'login server'.

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

    def __init__(self, address: tuple[str, int]) -> None:
        super().__init__(address=address)

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
        event_id = None

        if enet_event.type == enet.EVENT_TYPE_CONNECT:
            context.player = self.new_player(enet_event.peer)
            event_id = EventID.ON_CONNECT

        elif enet_event.type == enet.EVENT_TYPE_DISCONNECT:
            context.player = self.get_player(enet_event.peer)
            event_id = EventID.ON_DISCONNECT

            self.remove_player(enet_event.peer)

        elif enet_event.type == enet.EVENT_TYPE_RECEIVE:
            context.player = self.get_player(enet_event.peer)

            if Packet.get_type(enet_event.packet.data) == PacketType.TEXT:
                context.packet = TextPacket(enet_event.packet.data)
            elif Packet.get_type(enet_event.packet.data) == PacketType.GAME_MESSAGE:
                context.packet = GameMessagePacket(enet_event.packet.data)

            event_id = (
                context.packet.identify() if context.packet else EventID.ON_RECEIVE
            )

        if event_id is None:
            return False

        return await self.dispatch_event(event_id, context)
