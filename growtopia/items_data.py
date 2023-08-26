__all__ = ("ItemsData",)

from typing import Optional, Union

from .constants import ignored_attributes
from .error_manager import ErrorManager
from .exceptions import UnsupportedItemsData
from .file import File
from .item import Item
from .protocol import GameUpdatePacket, GameUpdatePacketType


class ItemsData(File):
    """
    Represents the items.dat file. Allows for easy access to item data.

    Parameters
    ----------
    data: Union[str, bytes]
        The data to parse. Can be a path to the file or bytes.

    Attributes
    ----------
    content: memoryview
        A memoryview of the raw bytes of the items.dat file.
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

    def __init__(self, data: Union[str, bytes]) -> None:
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

    async def parse(self) -> None:
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
        if not self.content:
            await self.read_file()

        data, offset = self.content, 6

        self.version = int.from_bytes(data[:2], "little")
        self.item_count = int.from_bytes(data[2:6], "little")

        if self.version not in list(ignored_attributes.keys()):
            ErrorManager._raise_exception(UnsupportedItemsData(self))

        for _ in range(self.item_count):
            item = Item()

            for attr in item.__dict__:
                if attr in ignored_attributes[self.version]:
                    continue

                if isinstance(item.__dict__[attr], int):
                    size = item.__dict__[attr]
                    item.__dict__[attr] = int.from_bytes(data[offset : offset + size], "little")
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
                        item.__dict__[attr] = "".join(chr(i) for i in data[offset : offset + str_len])

                    offset += str_len

                elif isinstance(item.__dict__[attr], bytearray):
                    item.__dict__[attr] = bytearray(
                        data[offset : offset + len(item.__dict__[attr])]
                    )  # create a new bytearray object to avoid users modifying the original bytearray that the memoryview object is referencing.
                    offset += len(item.__dict__[attr])

            self.items.append(item)

        self.hash_file()

    def get_item(
        self,
        item_id: Optional[int] = None,
        name: Optional[str] = None,
        *,
        _cache: dict[str, Item] = {},
    ) -> Optional[Item]:
        """
        Fetches an item from the items list. It is recommended to use the item's ID to fetch the item, as it is faster.

        Parameters
        ----------
        item_id: Optional[int]
            The ID of the item to fetch.
        name: Optional[str]
            The name of the item to fetch.

        Returns
        -------
        Optional[Item]
            The item that was fetched. If no item was found, returns None.

        Examples
        --------
        >>> from growtopia import ItemsData
        >>> items = ItemsData("items.dat")
        >>> items.get_item(1)
        """
        if item_id is not None and item_id < len(self.items):
            return self.items[item_id]

        if name is not None:
            if name.lower() in _cache:
                return _cache[name.lower()]

            for item in self.items:
                if item.name.lower() == name.lower():
                    if len(_cache) == 100:
                        _cache.popitem()

                    _cache[name.lower()] = item
                    return item

        return None

    def get_starts_with(
        self,
        val: str,
        _cache: dict[str, Item] = {},
    ) -> list[Item]:
        """
        Fetches all the items that start with the value provided.

        Parameters
        ----------
        val: str
            The value to match the start of the item's name with.

        Returns
        -------
        list[Item]
            A list of all the items that start with the value provided.

        Examples
        --------
        >>> from growtopia import ItemsData
        >>> items = ItemsData("items.dat")
        >>> items.get_starts_with("dirt")
        """
        if val in _cache:
            return _cache[val]

        if len(_cache) == 100:
            _cache.popitem()

        _cache[val] = (res := [item for item in self.items if item.name.lower().startswith(val.lower())])
        return res

    def get_ends_with(
        self,
        val: str,
        _cache: dict[str, Item] = {},
    ) -> list[Item]:
        """
        Fetches all the items that end with the value provided.

        Parameters
        ----------
        val: str
            The value to match the end of the item's name with.

        Returns
        -------
        list[Item]
            A list of all the items that end with the value provided.

        Examples
        --------
        >>> from growtopia import ItemsData
        >>> items = ItemsData("items.dat")
        >>> items.get_ends_with("lock")
        """
        if val in _cache:
            return _cache[val]

        if len(_cache) == 100:
            _cache.popitem()

        _cache[val] = (res := [item for item in self.items if item.name.lower().endswith(val.lower())])

        return res

    def get_contains(
        self,
        val: str,
        _cache: dict[str, Item] = {},
    ) -> list[Item]:
        """
        Fetches all the items that contain the value provided.

        Parameters
        ----------
        val: str
            The value to match the item's name with.

        Returns
        -------
        list[Item]
            A list of all the items that contain the value provided.

        Examples
        --------
        >>> from growtopia import ItemsData
        >>> items = ItemsData("items.dat")
        >>> items.get_contains("dirt")
        """
        if val in _cache:
            return _cache[val]

        if len(_cache) == 100:
            _cache.popitem()

        _cache[val] = (res := [item for item in self.items if val.lower() in item.name.lower()])

        return res

    @property
    def packet(self) -> GameUpdatePacket:
        """
        Returns the packet that should be sent to the client when it requests for the items.dat file.

        Returns
        -------
        GameUpdatePacket
            The packet that should be sent to the client when it requests for the items.dat file.

        Examples
        --------
        >>> from growtopia import ItemsData
        >>> items = ItemsData("items.dat")
        >>> items.packet
        """
        if not self.content:
            raise ValueError("The items.dat file has not been read yet.")

        return GameUpdatePacket(update_type=GameUpdatePacketType.SEND_ITEMS_DATA, extra_data=bytes(self.content))
