__all__ = ("World",)

from typing import TYPE_CHECKING, Optional

from ..constants import latest_game_version
from .tile import Tile
from .world_net import WorldNet
from .world_object import WorldObject

if TYPE_CHECKING:
    from ..player import Player


class World(WorldNet):
    def __init__(
        self,
        name: str,
        *,
        width: int = 100,
        height: int = 60,
        base_weather_id: int = 0,
        weather_id: int = 0,
        version: int = 20,
        flags: int = 64,
        spawn_pos: tuple[int, int] = (500, 500),
    ) -> None:
        super().__init__()

        self.name: str = name
        self.width: int = width
        self.height: int = height
        self.base_weather_id: int = base_weather_id
        self.weather_id: int = weather_id
        self.version: int = version
        self.flags: int = flags
        self.spawn_pos: tuple[int, int] = spawn_pos

        self.players: dict[int, Player] = {}
        self.tiles: list[Tile] = [Tile(pos=(i % self.width, i // self.width)) for i in range(width * height)]
        self.objects: list[WorldObject] = []

        self.__net_id: int = 0

    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        """
        Gets a tile at a position.

        Parameters
        ----------
        x: int
            The x position of the tile.
        y: int
            The y position of the tile.

        Returns
        -------
        Optional[Tile]:
            The tile if found, None otherwise.
        """
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None

        return self.tiles[x + y * self.width]

    def add_player(self, player: "Player", override_spawn: tuple[int, int] = None) -> bool:
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
        player.on_spawn(*(override_spawn or self.spawn_pos))
        player.pos = override_spawn or self.spawn_pos

        self.lambda_broadcast(
            lambda p: p.on_spawn(*(override_spawn or self.spawn_pos), player), exclude_net_id=player.net_id
        )

        for p in self.players.values():
            if p.net_id == player.net_id:
                continue

            player.on_spawn(*p.pos, p)

        self.__net_id += 1

        return True

    def get_player(self, net_id: int) -> Optional["Player"]:
        return self.players.get(net_id, None)

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
        """
        Creates a world from bytes.

        Parameters
        ----------
        data: bytes
            The bytes to create the world from.

        Keyword Arguments
        ----------
        game_version: float
            The game version to create the world for. (default latest_game_version)

        Returns
        -------
        Optional[World]:
            The world if successful, None otherwise.
        """
        world = cls()

        world.version = int.from_bytes(data[:2], "little")
        world.flags = int.from_bytes(data[2:6], "little")

        name_len = int.from_bytes(data[6:8], "little")
        world.name = data[8 : 8 + name_len].decode()

        world.width = int.from_bytes(data[8 + name_len : 12 + name_len], "little")
        world.height = int.from_bytes(data[12 + name_len : 16 + name_len], "little")

        tile_count = int.from_bytes(data[16 + name_len : 20 + name_len], "little")

        if game_version >= 4.31:
            data = data[20 + name_len :]

            data = data[13:]

        data = data[20 + name_len :]

        for _ in range(tile_count):
            tile = Tile.from_bytes(data[:20])
            world.tiles.append(tile)
            data = data[20:]

        if game_version >= 4.31:
            data = data[12:]

        obj_count = int.from_bytes(data[:4], "little")

        data = data[4:]

        for _ in range(obj_count):
            obj = WorldObject.from_bytes(data[:20])
            world.objects.append(obj)
            data = data[20:]

        world.base_weather_id = int.from_bytes(data[:4], "little")
        world.weather_id = int.from_bytes(data[4:8], "little")

        return world
