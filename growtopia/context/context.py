__all__ = ("Context",)


from typing import (
    TYPE_CHECKING,
    Optional,
    Union,
)

from enet import Event

if TYPE_CHECKING:
    from net import (
        HelloPacket,
        MessagePacket,
        TextPacket,
        UpdatePacket,
    )


class Context:
    def __init__(self) -> None:
        self.enet_event: Optional[Event] = None
        self.packet: Optional[Union[HelloPacket, TextPacket, MessagePacket, UpdatePacket]] = None
