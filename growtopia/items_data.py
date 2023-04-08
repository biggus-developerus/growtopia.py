__all__ = ("ItemsData",)

from functools import lru_cache
from typing import BinaryIO, Optional, Union

from .constants import ignored_attributes
from .exceptions import UnsupportedItemsData
from .item import Item
from .utils import decipher, hash_


class ItemsData:
    def __init__(self, data: Union[str, bytes, BinaryIO]) -> None:
        self.content: bytes

        if isinstance(data, str):
            with open(data, "rb") as f:
                self.content = f.read()
        elif isinstance(data, bytes):
            self.content = data
        elif isinstance(data, BinaryIO):
            self.content = data.read()
        else:
            raise ValueError("Invalid data type passed into initialiser.")

        self.items: dict[int, Item] = {}
        self.item_count: int = 0
        self.version: int = 0
        self.hash: int = 0

    def parse(self) -> None:
        data, offset = self.content, 6

        self.version = int.from_bytes(data[:2], "little")
        self.item_count = int.from_bytes(data[2:6], "little")

        if (
            self.version < list(ignored_attributes.keys())[0]
            or self.version > list(ignored_attributes.keys())[-1]
        ):
            raise UnsupportedItemsData(self)

        for _ in range(self.item_count):
            item = Item()

            for attr in item.__dict__:
                if attr in ignored_attributes[self.version]:
                    continue

                if isinstance(item.__dict__[attr], int):
                    size = item.__dict__[attr]
                    item.__dict__[attr] = int.from_bytes(
                        data[offset : offset + size], "little"
                    )
                    if attr == "break_hits":
                        item.__dict__[attr] = item.__dict__[attr] / 6
                    offset += size
                elif isinstance(item.__dict__[attr], str):
                    str_len = int.from_bytes(data[offset : offset + 2], "little")
                    offset += 2

                    if attr == "name":
                        item.__dict__[attr] = decipher(
                            "".join(chr(i) for i in data[offset : offset + str_len]),
                            item.id,
                        )
                    else:
                        item.__dict__[attr] = "".join(
                            chr(i) for i in data[offset : offset + str_len]
                        )

                    offset += str_len

                elif isinstance(item.__dict__[attr], bytearray):
                    item.__dict__[attr] = data[
                        offset : offset + len(item.__dict__[attr])
                    ]
                    offset += len(item.__dict__[attr])

            self.items[item.id] = item

        self.hash = hash_(data)

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
