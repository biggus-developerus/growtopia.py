__all__ = (
    "Inventory",
    "InventoryItem",
)

from dataclasses import dataclass

from .item import Item


@dataclass
class InventoryItem:
    """
    Represents an inventory item.

    Attributes
    ----------
    id: int
        The id of the item.
    count: int
        The count of the item.
    equipped: bool
        Whether the item's equipped or not.
    """

    id: int = 0
    count: int = 0
    equipped: bool = False

    def serialise(self) -> bytearray:
        """
        Serialises the inventory item.

        Returns
        -------
        bytearray
            The serialised inventory item.
        """

        return bytearray(
            self.id.to_bytes(2, "little") + self.count.to_bytes(1, "little") + self.equipped.to_bytes(1, "little")
        )

    @classmethod
    def from_bytes(cls, data: bytearray) -> "InventoryItem":
        """
        Creates a new inventory item from the given data.

        Parameters
        ----------
        data: bytearray
            The data to create the inventory item from.

        Returns
        -------
        InventoryItem
            The created inventory item.
        """

        item = cls()

        item.id = int.from_bytes(data[0:2], "little")
        item.count = int.from_bytes(data[2:3], "little")
        item.equipped = bool.from_bytes(data[3:4], "little")

        return item


class Inventory:
    """
    Represents an Inventory.

    Attributes
    ----------
    version: int
        The version of the inventory format.
    slots: int
        Represents the slots in the inventory (count).
    """

    def __init__(self) -> None:
        self.version: int = 20  # uint8
        self.slots: int = 10  # uint32

        self.items: dict[int, InventoryItem] = {}  # item_id: InventoryItem

    def add_item(self, item_id_or_item: int | Item, count: int, equipped: bool = False) -> None:
        """
        Adds an item to the inventory.

        Parameters
        ----------
        item_id_or_item: Union[int, Item]
            The id of the item or Item object to add.
        count: int
            The count of the item to add.
        equipped: bool
            Whether the item's equipped or not. (default False)
        """
        item_id = item_id_or_item if isinstance(item_id_or_item, int) else item_id_or_item.id

        if item_id in self.items:
            self.items[item_id].count += count
            return

        item = InventoryItem(item_id, count, equipped)
        self.items[item.id] = item

    def remove_item(self, item_id: int, count: int) -> None:
        """
        Removes an item from the inventory.

        Parameters
        ----------
        item_id: int
            The id of the item to remove.
        count: int
            The count of the item to remove.
        """

        item = self.items.get(item_id, None)

        if not item:
            return

        item.count -= count

        if item.count <= 0:
            self.items.pop(item_id)

    def serialise(self) -> bytearray:
        """
        Serialises the inventory.

        Returns
        -------
        bytearray
            The serialised inventory.
        """

        data = bytearray(self.version.to_bytes(1, "little"))
        data += bytearray(self.slots.to_bytes(4, "little"))
        data += bytearray(len(self.items).to_bytes(2, "little"))

        for item in self.items.values():
            data += item.serialise()

        return data

    @classmethod
    def from_bytes(cls, data: bytearray) -> "Inventory":
        """
        Creates a new inventory from the given data.

        Parameters
        ----------
        data: bytearray
            The data to create the inventory from.

        Returns
        -------
        Inventory
            The created inventory.
        """

        inventory = cls()

        inventory.version = data[0]
        inventory.slots = int.from_bytes(data[1:5], "little")

        item_count = int.from_bytes(data[5:6], "little")
        offset = 6

        for _ in range(item_count):
            item = InventoryItem.from_bytes(data[offset : offset + 4])
            inventory.items[item.id] = item

            offset += 4

        return inventory
