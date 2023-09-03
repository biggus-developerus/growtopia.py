__all__ = ("WorldTilePool",)

from abc import ABC, abstractmethod

from typing import Optional, Union
from ..item import Item
from .tile import Tile


class WorldTilePool(ABC):
    def __init__(self, width: int, height: int) -> None:
        self.tiles: list[Tile] = [Tile(pos=(i % width, i // width)) for i in range(width * height)]

    @property
    @abstractmethod
    def width(self) -> int:
        ...

    @property
    @abstractmethod
    def height(self) -> int:
        ...

    def set_row_tiles(
        self,
        row: int,
        foreground_item_or_item_id: Optional[Union[Item, int]] = 0,
        background_item_or_item_id: Optional[Union[Item, int]] = 0,
    ) -> None:
        """
        Sets a row of tiles.

        Parameters
        ----------
        row: int
            The row to set.
        foreground_item_or_item_id: Optional[Union[Item, int]]
            The foreground item or item id to set. (default 0)
        background_item_or_item_id: Optional[Union[Item, int]]
            The background item or item id to set. (default 0)
        """
        foreground = (
            foreground_item_or_item_id if isinstance(foreground_item_or_item_id, int) else foreground_item_or_item_id.id
        )
        background = (
            background_item_or_item_id if isinstance(background_item_or_item_id, int) else background_item_or_item_id.id
        )

        for tile in self.get_row(row):
            tile.foreground = foreground
            tile.background = background

    def set_column_tiles(
        self,
        column: int,
        foreground_item_or_item_id: Optional[Union[Item, int]] = 0,
        background_item_or_item_id: Optional[Union[Item, int]] = 0,
    ) -> None:
        """
        Sets a column of tiles.

        Parameters
        ----------
        column: int
            The column to set.
        foreground_item_or_item_id: Optional[Union[Item, int]]
            The foreground item or item id to set. (default 0)
        background_item_or_item_id: Optional[Union[Item, int]]
            The background item or item id to set. (default 0)
        """
        foreground = (
            foreground_item_or_item_id if isinstance(foreground_item_or_item_id, int) else foreground_item_or_item_id.id
        )
        background = (
            background_item_or_item_id if isinstance(background_item_or_item_id, int) else background_item_or_item_id.id
        )

        for tile in self.get_column(column):
            tile.foreground = foreground
            tile.background = background

    def get_row(self, row: int, start: Optional[int] = 0, end: Optional[int] = 0) -> list[Tile]:
        """
        Gets a row of tiles.

        Parameters
        ----------
        row: int
            The row to get.
        start: Optional[int]
            The start of the row to get. (default 0)
        end: Optional[int]
            The end of the row to get. (default 0)

        Returns
        -------
        list[Tile]:
            The row of tiles.
        """
        return self.tiles[row * self.width + start : row * self.width + (end or self.width)]

    def get_column(self, column: int, start: Optional[int] = 0, end: Optional[int] = 0) -> list[Tile]:
        """
        Gets a column of tiles.

        Parameters
        ----------
        column: int
            The column to get.
        start: Optional[int]
            The start of the column to get. (default 0)
        end: Optional[int]
            The end of the column to get. (default 0)

        Returns
        -------
        list[Tle]:
            The column of tiles.
        """
        return [self.tiles[i * self.width + column + start] for i in range((end or self.height))]

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
