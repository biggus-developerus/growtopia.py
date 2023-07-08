__all__ = ("Context",)

from typing import TYPE_CHECKING, Optional, Union

import enet

if TYPE_CHECKING:
    from .client import Client
    from .player import Player
    from .protocol import (
        GameMessagePacket,
        GameUpdatePacket,
        HelloPacket,
        Packet,
        TextPacket,
    )
    from .server import Server


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
    packet: Optional[Union["Packet","GameUpdatePacket","GameMessagePacket","TextPacket","HelloPacket"]
        The packet that was emitted.
    """

    def __init__(self) -> None:
        # Servers (main game server, login server, proxy server, etc.)
        self.server: Optional["Server"] = None

        # Clients (main game client, proxy client, etc.)
        self.client: Optional["Client"] = None

        # Other objects (Player, World, enet.Event, etc.)
        self.player: Optional["Player"] = None
        self.enet_event: Optional[enet.Event] = None
        self.packet: Optional[
            Union[
                "Packet",
                "GameUpdatePacket",
                "GameMessagePacket",
                "TextPacket",
                "HelloPacket",
            ]
        ] = None
