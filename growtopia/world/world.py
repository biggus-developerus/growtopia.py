__all__ = ("World",)

from typing import TYPE_CHECKING, Callable, Optional, Union

from ..constants import latest_game_version
from ..protocol import GameMessagePacket, GameUpdatePacket, Packet, TextPacket
from .tile import Tile
from .world_avatar_pool import WorldAvatarPool
from .world_object import WorldObject
from .world_player_pool import WorldPlayerPool
from .world_tile_pool import WorldTilePool

if TYPE_CHECKING:
    from ..avatar import Avatar


class World(WorldAvatarPool, WorldPlayerPool, WorldTilePool):
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
        spawn_pos: tuple[int, int] = (0, 0),
    ) -> None:
        WorldAvatarPool.__init__(self)
        WorldPlayerPool.__init__(self)
        WorldTilePool.__init__(self, width, height)

        self.name: str = name
        self.__width: int = width
        self.__height: int = height
        self.base_weather_id: int = base_weather_id
        self.weather_id: int = weather_id
        self.version: int = version
        self.flags: int = flags
        self.__spawn_pos: tuple[int, int] = spawn_pos

        self.avatars: dict[int, "Avatar"] = {}
        self.objects: list[WorldObject] = []

        self.__next_net_id: int = 0

    @property
    def width(self) -> int:
        """
        Returns the width of the world.

        Returns
        -------
        int:
            The width of the world.
        """
        return self.__width

    @width.setter
    def width(self, value: int) -> None:
        """
        Sets the width of the world.

        Parameters
        ----------
        value: int
            The width to set.
        """
        self.__width = value

    @property
    def height(self) -> int:
        """
        Returns the height of the world.

        Returns
        -------
        int:
            The height of the world.
        """
        return self.__height

    @height.setter
    def height(self, value: int) -> None:
        """
        Sets the height of the world.

        Parameters
        ----------
        value: int
            The height to set.
        """
        self.__height = value

    @property
    def spawn_pos(self) -> tuple[int, int]:
        """
        Returns the spawn position of the world.

        Returns
        -------
        tuple[int, int]:
            The spawn position of the world.
        """
        return self.__spawn_pos

    @spawn_pos.setter
    def spawn_pos(self, value: tuple[int, int]) -> None:
        """
        Sets the spawn position of the world.

        Parameters
        ----------
        value: tuple[int, int]
            The spawn position to set.
        """
        self.__spawn_pos = value

    @property
    def next_net_id(self) -> int:
        """
        Returns the net ID of the next player.

        Returns
        -------
        int:
            The net ID of the next player.
        """
        return self.__next_net_id

    @next_net_id.setter
    def next_net_id(self, value: int) -> None:
        """
        Sets the net ID of the next player.

        Parameters
        ----------
        value: int
            The net ID to set.
        """
        self.__next_net_id = value

    def broadcast(
        self, packet: Union[Packet, GameUpdatePacket, GameMessagePacket, TextPacket], exclude_net_id: int = -1
    ) -> None:
        """
        Broadcasts a packet to all players in the world.

        Parameters
        ----------
        packet: Union[Packet, GameUpdatePacket, GameMessagePacket, TextPacket]
            The packet to broadcast.
        """
        for player in self.players.values():
            if player.net_id == exclude_net_id:
                continue

            player.send(packet)

    def lambda_broadcast(self, callback: Callable, exclude_net_id: int = -1) -> None:
        """
        Calls a callback for each player in the world.

        Parameters
        ----------
        callback: Callable(Player)
            The callback to call for each player.
        """
        for player in self.players.values():
            if player.net_id == exclude_net_id:
                continue

            callback(player)

    def kill_avatar(self, avatar: "Avatar", respawn: bool = True) -> None:
        """
        Kills an avatar.

        Parameters
        ----------
        respawn: bool
            Whether the avatar should return to the world's spawn position or not.
        """
        self.lambda_broadcast(lambda p: p.on_killed(avatar))

        if respawn:
            self.lambda_broadcast(lambda p: p.set_pos(*self.spawn_pos, avatar))

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
