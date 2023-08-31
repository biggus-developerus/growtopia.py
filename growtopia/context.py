__all__ = (
    "Context",
    "ServerContext",
    "ClientContext",
)

from typing import TYPE_CHECKING, Optional, Union

import enet

if TYPE_CHECKING:
    from .clients import Client, GameClient
    from .item import Item
    from .items_data import ItemsData
    from .player import Player
    from .player_tribute import PlayerTribute
    from .protocol import (
        GameMessagePacket,
        GameUpdatePacket,
        HelloPacket,
        StrPacket,
        TextPacket,
    )
    from .servers import Server
    from .world import Tile, World


class Context:
    """
    A class that is instantiated when a proper event is emitted. This class is used to store data that is passed to
    the event handler.

    Attributes
    ----------
    server: Optional[:class:`Server`]
        The server that emitted the event.
    player: Optional[:class:`Player`]
        The player that emitted the event.
    enet_event: Optional[:class:`Event`]
        The event that was emitted.
    packet: Optional[Union["StrPacket","GameUpdatePacket","GameMessagePacket","TextPacket","HelloPacket"]
        The packet that was emitted.
    """

    def __init__(self) -> None:
        self.enet_event: Optional[enet.Event] = None
        self.packet: Optional[
            Union[
                "StrPacket",
                "GameUpdatePacket",
                "GameMessagePacket",
                "TextPacket",
                "HelloPacket",
            ]
        ] = None


class ClientContext(Context):
    def __init__(self) -> None:
        super().__init__()

        self.client: Optional[Union["Client", "GameClient"]] = None

    def reply(self, packet: Union["StrPacket", "GameUpdatePacket", "HelloPacket"]) -> bool:
        return self.client.send(packet)


class ServerContext(Context):
    def __init__(self) -> None:
        super().__init__()

        self.server: Optional["Server"] = None
        self.player: Optional["Player"] = None
        self.world: Optional["World"] = None
        self.tile: Optional["Tile"] = None
        self.items_data: Optional["ItemsData"] = None
        self.item: Optional["Item"] = None
        self.player_tribute: Optional["PlayerTribute"] = None

    def reply(self, packet: Union["StrPacket", "GameUpdatePacket", "HelloPacket"]) -> bool:
        """
        Replies to the player with a packet.

        Parameters
        ----------
        packet: Union[`StrPacket`, `GameUpdatePacket`, `HelloPacket`]
            The packet to reply with.

        Returns
        -------
        bool
            Whether the packet was sent successfully.
        """
        return self.player.send(packet)
