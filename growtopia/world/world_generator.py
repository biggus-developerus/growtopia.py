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

        DIRT: Item = ObjHolder.items_data.get_item("Dirt")
        CAVE_BACKGROUND: Item = ObjHolder.items_data.get_item("Cave Background")
        BEDROCK: Item = ObjHolder.items_data.get_item("Bedrock")

        for y in range(world.height // 2, world.height):
            # Base
            world.set_row_tiles(y, DIRT, CAVE_BACKGROUND)

            # Bedrock
            if y >= world.height - 6:
                world.set_row_tiles(y, BEDROCK, CAVE_BACKGROUND)

        # Main Door
        world.get_tile(*world.spawn_pos).set_item(ObjHolder.items_data.get_item("Main Door"), door_label="EXIT")
        world.get_tile(world.spawn_pos[0], world.spawn_pos[1] + 1).set_item(BEDROCK)

        return world
