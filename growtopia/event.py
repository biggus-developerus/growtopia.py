__all__ = ("Event",)

import time
from typing import TYPE_CHECKING, Optional

import enet

if TYPE_CHECKING:
    from .player import Player


class Event:
    """
    Represents an event that is emitted by the dispatcher.

    Parameters
    ----------
    enet_event: enet.Event
        The ENet event that was emitted.

    Attributes
    ----------
    enet_event: enet.Event
        The ENet event that was emitted.
    timestamp: float
        The timestamp of when the event was emitted.
    handled: bool
        Whether or not the event has been handled.
    """

    def __init__(self, enet_event: enet.Event) -> None:
        self.enet_event: enet.Event = enet_event
        self.timestamp: float = time.time()

        self.handled: bool = False
        self.sent_to: Optional["Player"] = None
