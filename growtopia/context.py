__all__ = ("Context",)

from typing import TYPE_CHECKING, Optional

import enet

if TYPE_CHECKING:
    from .client import Client
    from .server import Server


class Context:
    def __init__(self) -> None:
        # enet
        self.event: Optional[enet.Event] = None
        self.peer: Optional[enet.Peer] = None
        self.enet_packet: Optional[enet.Packet] = None

        # objects
        self.server: Optional["Server"] = None
        self.client: Optional["Client"] = None
