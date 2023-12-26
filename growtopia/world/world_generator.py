__all__ = ['WorldGenerator']


from .world import World
from ..items_data import ItemsData
from .tile import Tile


class WorldGenerator:
	def __init__(self) -> None:
		pass


	@staticmethod
	def default(world: World, items_data: ItemsData) -> World:
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

		spawn_pos: tuple[int, int] = world.spawn_pos

		# Dirt & Bedrock
		for y in range(50, 100):
			if y >= 94:
				world.set_row_tiles(
					y,
					items_data.get_item(name="Bedrock")
				)

				continue

			world.set_row_tiles(
				y,
				items_data.get_item(name="Dirt"),
				items_data.get_item(name="Cave Background")
			)

		# Main Door
		for x in range(world.width):
			new_tile = Tile()

			for y in range(world.height):
				new_tile.pos = (x, y)

				# Door
				if (x, y) == spawn_pos:
					new_tile.foreground = items_data.get_item(name="Main Door")

				# Bedrock
				if (x, y) == (spawn_pos + (0, 1)):
					new_tile.foreground = items_data.get_item(name="Bedrock")

			world.tiles[x * y] = new_tile

		return world