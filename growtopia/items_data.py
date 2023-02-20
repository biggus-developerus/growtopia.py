__all__ = ("ItemsData",)

from functools import lru_cache
from typing import Optional

from .item import Item


class ItemsData:
    def __init__(self, path: str) -> None:
        with open(path, "rb") as f:
            self.content: bytes = f.read()

        self.items: dict[int, Item] = {}
        self.item_count: int = 0
        self.version: int = 0
        self.hash: int = 0

    @lru_cache(maxsize=None)
    def get_item(self, item_id: int = None, name: str = None) -> Optional[Item]:
        if item_id is not None:
            return self.items.get(item_id, None)

        if name is not None:
            for item in list(self.items.values()):
                if item.name.lower() == name.lower():
                    return item

        return None

    @lru_cache(maxsize=None)
    def get_starts_with(self, name: str) -> list[Item]:
        return [
            item
            for item in list(self.items.values())
            if item.name.lower().startswith(name.lower())
        ]

    @lru_cache(maxsize=None)
    def get_ends_with(self, name: str) -> list[Item]:
        return [
            item
            for item in list(self.items.values())
            if item.name.lower().endswith(name.lower())
        ]

    @lru_cache(maxsize=None)
    def get_contains(self, name: str) -> list[Item]:
        return [
            item
            for item in list(self.items.values())
            if name.lower() in item.name.lower()
        ]
