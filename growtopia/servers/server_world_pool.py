__all__ = ("ServerWorldPool",)

from ..world import World


class ServerWorldPool:
	def __init__(self) -> None:
		self.worlds: dict[str, World] = {}  # worlds by name

	def new_world(
		self,
		name: str,
		*,
		width: int = 100,
		height: int = 60,
		base_weather_id: int = 0,
		weather_id: int = 0,
	) -> World:
		"""
		Creates a new world and adds it to the worlds dict.

		Parameters
		----------
		name: str
			The name of the world to create.

		Returns
		-------
		World:
			The world that was created.
		"""
		world = World(name, width=width, height=height, base_weather_id=base_weather_id, weather_id=weather_id)
		self.worlds[name] = world

		return world

	def add_world(self, world: World) -> bool:
		"""
		Adds a world to the pool.

		Parameters
		----------
		world: World
			The world to add.

		Returns
		-------
		bool:
			True if the world was successfully added, False otherwise.
		"""
		if world.name in self.worlds:
			return False

		self.worlds[world.name] = world

		return True

	def remove_world(self, world: World) -> bool:
		"""
		Removes a world from the pool.

		Parameters
		----------
		world: World
			The world to remove.

		Returns
		-------
		bool:
			True if the world was successfully removed, False otherwise.
		"""
		if world.name not in self.worlds:
			return False

		del self.worlds[world.name]

		return True

	def get_world(self, name: str) -> World:
		"""
		Gets a world from the pool.

		Parameters
		----------
		name: str
			The name of the world to get.

		Returns
		-------
		Optional[World]:
			The world if it was found, None otherwise.
		"""
		return self.worlds.get(name, None)
