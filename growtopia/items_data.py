__all__ = ("ItemsData",)

from functools import lru_cache
from typing import BinaryIO, Optional, Union

from .constants import ignored_attributes
from .exceptions import UnsupportedItemsData
from .file import File
from .item import Item


class ItemsData(File):
    """
    Represents the items.dat file. Allows for easy access to item data.

    Parameters
    ----------
    data: Union[str, bytes, BinaryIO]
        The data to parse. Can be a path to the file, bytes, or a file-like object.

    Attributes
    ----------
    content: bytes
        The raw bytes of the items.dat file.
    items: list[Item]
        A list of all the items in the items.dat file.
    item_count: int
        The amount of items in the items.dat file.
    version: int
        The version of the items.dat file.
    hash: int
        The hash of the items.dat file.

    Raises
    ------
    ValueError
        Invalid data type passed into initialiser.

    Examples
    --------
    >>> from growtopia import ItemsData
    >>> items = ItemsData("items.dat")
    >>> items.get_item(1)
    """

    def __init__(self, data: Union[str, bytes, BinaryIO]) -> None:
        super().__init__(data)

        self.items: list[Item] = []
        self.item_count: int = 0
        self.version: int = 0

    @classmethod
    def from_bytes(cls, data: bytes) -> "ItemsData":
        """
        Instantiates the class with the raw bytes provided.

        Parameters
        ----------
        data: bytes
            The raw data of the items.dat file.

        Raises
        ------
        ValueError
            Invalid data type passed into initialiser.

        Returns
        -------
        ItemsData
            The instance of the class.
        """
        return cls(data)

    @classmethod
    def decrypt(cls, name: str, key: int) -> str:
        """
        Decrypts the name of an item.

        Parameters
        ----------
        name: str
            The name of the item to decrypt.
        key: int
            The key to use to decrypt the name. This is usually the item's ID.

        Returns
        -------
        result: str
            The decrypted name.
        """
        key %= (key_len := len("*PBG892FXX982ABC"))
        result = ""

        for i in name:
            result += chr(ord(i) ^ ord("PBG892FXX982ABC*"[key]))
            key += 1

            if key >= key_len:
                key = 0

        return result

    def parse(self) -> None:
        """
        Parses the contents passed into the initialiser.
        This method is better called once, as it is quite slow.
        Try to store the instance of this class somewhere and reuse it.


        Raises
        ------
        UnsupportedItemsData
            The items.dat file is not supported by this library. Raised when the version of the items.dat file is not supported.

        Returns
        -------
        None
        """
        data, offset = self.content, 6

        self.version = int.from_bytes(data[:2], "little")
        self.item_count = int.from_bytes(data[2:6], "little")

        if (
            self.version < list(ignored_attributes.keys())[0]
            or self.version > list(ignored_attributes.keys())[-1]
            or self.version not in ignored_attributes
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
                        item.__dict__[attr] = self.decrypt(
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

            self.items.append(item)

        self.hash_file()

    @lru_cache(maxsize=100)
    def get_item(self, item_id: int = None, name: str = None) -> Optional[Item]:
        if item_id is not None and item_id < len(self.items):
            return self.items[item_id]

        if name is not None:
            for item in self.items:
                if item.name.lower() == name.lower():
                    return item

        return None

    @lru_cache(maxsize=100)
    def get_starts_with(self, name: str) -> list[Item]:
        return [
            item for item in self.items if item.name.lower().startswith(name.lower())
        ]

    @lru_cache(maxsize=100)
    def get_ends_with(self, name: str) -> list[Item]:
        return [item for item in self.items if item.name.lower().endswith(name.lower())]

    @lru_cache(maxsize=100)
    def get_contains(self, name: str) -> list[Item]:
        return [item for item in self.items if name.lower() in item.name.lower()]
