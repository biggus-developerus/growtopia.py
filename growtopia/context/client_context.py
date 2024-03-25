__all__ = ("ClientContext",)


from typing import (
    TYPE_CHECKING,
    Optional,
    Union,
)

from .context import Context

if TYPE_CHECKING:
    from net import (
        Client,
        GameClient,
        HelloPacket,
        MessagePacket,
        TextPacket,
        UpdatePacket,
    )


class ClientContext(Context):
    def __init__(self) -> None:
        super().__init__()

        self.client: Optional[Union[Client, GameClient]] = None

    def reply(self, packet: Union[HelloPacket, TextPacket, MessagePacket, UpdatePacket]) -> bool:
        return self.client.send(packet)
