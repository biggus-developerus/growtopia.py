__all__ = (
    "Inventory",
    "InventoryItem",
)

from dataclasses import dataclass


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
    Represents a client's inventory (set upon emitting ON_SEND_INVENTORY_STATE).

    Attributes
    ----------
    version: int
        The version of the inventory format.
    slots: int
        Represents the slots in the inventory (count).
    item_count: int


    """

    def __init__(self) -> None:
        self.version: int = 0  # uint8
        self.slots: int = 0  # uint32

        self.items: list[InventoryItem] = []

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

        for item in self.items:
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
        inventory.item_count = int.from_bytes(data[5:6], "little")

        offset = 6

        for _ in range(inventory.item_count):
            item = InventoryItem.from_bytes(data[offset : offset + 4])
            inventory.items.append(item)

            offset += 4

        return inventory
