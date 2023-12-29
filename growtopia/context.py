from __future__ import annotations

__all__ = (
    "Context",
    "ServerContext",
    "ClientContext",
)

from typing import TYPE_CHECKING

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
        self.enet_event: enet.Event | None = None
        self.packet: "StrPacket" | "GameUpdatePacket" | "GameMessagePacket" | "TextPacket" | "HelloPacket" | None = None


class ClientContext(Context):
    def __init__(self) -> None:
        super().__init__()

        self.client: "Client" | "GameClient" | None = None

    def reply(self, packet: "StrPacket" | "GameUpdatePacket" | "HelloPacket") -> bool:
        return self.client.send(packet)


class ServerContext(Context):
    def __init__(self) -> None:
        super().__init__()

        self.server: "Server" | None = None
        self.player: "Player" | None = None
        self.world: "World" | None = None
        self.tile: "Tile" | None = None
        self.items_data: "ItemsData" | None = None
        self.item: "Item" | None = None
        self.player_tribute: "PlayerTribute" | None = None

    def reply(self, packet: "StrPacket" | "GameUpdatePacket" | "HelloPacket") -> bool:
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
