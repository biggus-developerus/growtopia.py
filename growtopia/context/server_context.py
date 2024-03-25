__all__ = ("ServerContext",)


from typing import (
    TYPE_CHECKING,
    Optional,
    Union,
)

from .context import Context

if TYPE_CHECKING:
    from net import (
        HelloPacket,
        MessagePacket,
        Player,
        Server,
        TextPacket,
        UpdatePacket,
    )
    from parsers import (
        Item,
        ItemsData,
        PlayerTribute,
    )
    from world import (
        Tile,
        World,
    )


class ServerContext(Context):
    def __init__(self) -> None:
        super().__init__()

        self.server: Optional[Server] = None
        self.player: Optional[Player] = None
        self.world: Optional[World] = None
        self.tile: Optional[Tile] = None
        self.items_data: Optional[ItemsData] = None
        self.item: Optional[Item] = None
        self.player_tribute: Optional[PlayerTribute] = None

    def reply(self, packet: Union[HelloPacket, TextPacket, MessagePacket, UpdatePacket]) -> bool:
        return self.player.send(packet)
