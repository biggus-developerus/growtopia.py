__all__ = ("WorldTilePool",)

from .tile import Tile


class WorldTilePool:
    def __init__(self, width: int, height: int) -> None:
        self.tiles: list[Tile] = [Tile() for _ in range(width * height)]
