from __future__ import annotations

__all__ = ["WorldGenerator"]

from ..item import Item
from ..obj_holder import ObjHolder
from .tile import Tile
from .world import World


class WorldGenerator:
    def __init__(self) -> None:
        pass

    @staticmethod
    def default(world: World) -> World:
        """
        Creates a default world.

        Arguments
        ---------
                world: growtopia.World - The world to modify.
                items_data: growtopia.ItemsData - The server's items data.

        Returns
        -------
                world <growtopia.World> - The modified world.
        """

        CAVE_BACKGROUND: Item = ObjHolder.items_data.get_item("Cave Background")
        BEDROCK: Item = ObjHolder.items_data.get_item("Bedrock")

        for y in range(world.height // 2, world.height):
            # Base
            world.set_row_tiles(y, ObjHolder.items_data.get_item("Dirt"), CAVE_BACKGROUND)

            # Bedrock
            if y >= world.height - 6:
                world.set_row_tiles(y, BEDROCK, CAVE_BACKGROUND)

        # Main Door
        for y in range(world.height):
            for x in range(world.width):
                new_tile = Tile(pos=world.spawn_pos)

                # Door
                if (x, y) == world.spawn_pos:
                    new_tile.foreground = ObjHolder.items_data.get_item("Main Door")

                # Bedrock
                if (x, y) == (world.spawn_pos + (0, 1)):
                    new_tile.foreground(BEDROCK)

                world.tiles[x * y] = new_tile

        return world
