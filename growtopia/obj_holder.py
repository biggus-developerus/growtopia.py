__all__ = ("ObjHolder")

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from .items_data import ItemsData
	from .item import Item
	from .player_tribute import PlayerTribute


class ObjHolder:
	"""
	Holds some global objects. Used to avoid the need to pass them around everywhere.
	"""
	
	items_data: "ItemsData"
	player_tribute: "PlayerTribute"