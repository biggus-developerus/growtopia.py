__all__ = ("Context",)

from typing import TYPE_CHECKING, Optional

import enet

if TYPE_CHECKING:
    from .event import Event
    from .player import Player
    from .protocol import Packet
    from .server import Server


class Context:
    """
    A class that is instantiated when a proper event is emitted. This class is used to store data that is passed to
    the event handler.  

    Attributes
    ----------
    """

    def __init__(self) -> None:
        # Servers (main game server, login server, proxy server, etc.)
        self.server: Optional["Server"] = None

        # Other objects (Player, World, Event, etc.)
        self.player: Optional["Player"] = None
        self.event: Optional["Event"] = None
        self.packet: Optional["Packet"] = None
