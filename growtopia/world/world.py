__all__ = ("World",)

from typing import TYPE_CHECKING, Optional

from ..constants import latest_game_version
from ..protocol import (
    GameMessagePacket,
    GameUpdatePacket,
    GameUpdatePacketFlags,
    GameUpdatePacketType,
    Packet,
    TextPacket,
    VariantList,
)
from .tile import Tile
from .world_net import WorldNet
from .world_object import WorldObject

if TYPE_CHECKING:
    from ..player import Player


class World(WorldNet):
    def __init__(self) -> None:
        super().__init__()

        self.version: int = 20  # uint16
        self.flags: int = 64  # uint32

        self.name: str = ""

        self.width: int = 100  # uint32
        self.height: int = 60  # uin32

        self.base_weather_id: int = 0  # uint32
        self.weather_id: int = 0  # uint32

        self.data: bytearray = bytearray()

        self.players: dict[int, "Player"] = {}  # players by net id
        self.tiles: list[Tile] = [Tile() for _ in range(self.width * self.height)]
        self.objects: list[WorldObject] = []

        self.__net_id: int = 0  # incremented upon adding a player (never decremented or reset)

    def add_player(self, player: "Player") -> bool:
        """
        Adds a player to the world.

        Parameters
        ----------
        player: Player
            The player to add to the world.

        Returns
        -------
        bool:
            True if the player was added, False otherwise.
        """
        if player.net_id in self.players:
            return False

        if player.world == None:
            player.world = self

        player.net_id = self.__net_id
        self.players[player.net_id] = player

        player._send_world(self)
        player.on_spawn(500, 500)

        self.lambda_broadcast(lambda p: p.on_spawn(500, 500, player), exclude_net_id=player.net_id)

        for p in self.players.values():
            if p.net_id == player.net_id:
                continue

            player.on_spawn(500, 500, p)

        self.__net_id += 1

        return True

    def remove_player(self, player: "Player") -> bool:
        """
        Removes a player from the world.

        Parameters
        ----------
        player: Player
            The player to remove from the world.

        Returns
        -------
        bool:
            True if the player was removed, False otherwise.
        """
        if player.net_id not in self.players:
            return False

        del self.players[player.net_id]

        self.lambda_broadcast(lambda p: p._on_remove(player), exclude_net_id=player.net_id)

        return True

    def serialise(self, *, game_version: float = latest_game_version) -> bytearray:
        """
        Serialises the world.

        Keyword Arguments
        ----------
        game_version: float
            The game version to serialise the world for. (default latest_game_version)

        Returns
        -------
        bytearray:
            The serialised world.
        """
        self.data = bytearray()

        self.data += self.version.to_bytes(2, "little")
        self.data += self.flags.to_bytes(4, "little")

        self.data += len(self.name).to_bytes(2, "little")
        self.data += self.name.encode()

        self.data += self.width.to_bytes(4, "little")
        self.data += self.height.to_bytes(4, "little")

        self.data += len(self.tiles).to_bytes(4, "little")

        if game_version >= 4.31:
            self.data += int(0).to_bytes(4, "little")
            self.data += int(0).to_bytes(1, "little")

        for tile in self.tiles:
            self.data += tile.serialise()

        if game_version >= 4.31:
            self.data += int(0).to_bytes(8, "little")
            self.data += int(0).to_bytes(4, "little")

        self.data += len(self.objects).to_bytes(4, "little")
        self.data += int(0).to_bytes(4, "little")

        for obj in self.objects:
            self.data += obj.serialise()

        self.data += self.base_weather_id.to_bytes(4, "little")
        self.data += self.weather_id.to_bytes(4, "little")

        return self.data

    @classmethod
    def from_bytes(cls, data: bytes, *, game_version: float = latest_game_version) -> Optional["World"]:
        raise NotImplementedError
