__all__ = ("Context",)

from typing import TYPE_CHECKING, Optional

import enet

if TYPE_CHECKING:
    from .client import Client
    from .player import Player
    from .protocol import Packet
    from .server import Server


class Context:
    def __init__(self) -> None:
        # enet
        self.event: Optional[enet.Event] = None
        self.peer: Optional[enet.Peer] = None
        self.enet_packet: Optional[enet.Packet] = None

        # main objects (server, client)
        self.server: Optional["Server"] = None
        self.client: Optional["Client"] = None

        # other objects (player, world, etc)
        self.player: Optional["Player"] = None

        # protocol
        self.packet: Optional["Packet"] = None
