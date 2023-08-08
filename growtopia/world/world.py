__all__ = ("World",)

from typing import Optional

from ..constants import latest_game_version
from ..player import Player
from .tile import Tile
from .world_net import WorldNet
from .world_object import WorldObject


class World(WorldNet):
    def __init__(self) -> None:
        super().__init__()

        self.players: dict[str, Player] = {}  # players by address

        self.version: int = 20  # uint16
        self.flags: int = 64  # uint32

        self.name: str = ""

        self.width: int = 100  # uint32
        self.height: int = 60  # uin32

        self.base_weather_id: int = 0  # uint32
        self.weather_id: int = 0  # uint32

        self.data: bytearray = bytearray()

        self.tiles: list[Tile] = [Tile() for _ in range(self.width * self.height)]
        self.objects: list[WorldObject] = []

    def serialise(self, *, game_version: float = latest_game_version) -> bytearray:
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
