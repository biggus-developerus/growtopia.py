__all__ = (
    "Inventory",
    "InventoryItem",
)

from dataclasses import dataclass


@dataclass
class InventoryItem:
    """
    Represents an inventory item.
    """

    id: int = 0  # uint16
    count: int = 0  # uint8
    equipped: bool = False  # uint8

    def to_bytes(self) -> bytearray:
        """
        Converts the inventory item to bytes.

        Returns
        -------
        bytearray
            The converted inventory item.
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
        item.count = data[3]
        item.equipped = data[4]

        return item

    def to_bytes(self) -> bytearray:
        """
        Converts the inventory item to bytes.

        Returns
        -------
        bytearray
            The converted inventory item.
        """

        return bytearray(
            self.id.to_bytes(2, "little") + self.count.to_bytes(1, "little") + self.equipped.to_bytes(1, "little")
        )


class Inventory:
    """
    Represents a client's inventory (set upon emitting ON_SEND_INVENTORY_STATE).
    """

    def __init__(self) -> None:
        self.version: int = 0  # uint8
        self.slots: int = 0  # uint32
        self.item_count: int = 0  # uint16

        self.items: list[InventoryItem] = []

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
        inventory.item_count = int.from_bytes(data[5:7], "little")

        offset = 7

        for _ in range(inventory.item_count):
            item = InventoryItem.from_bytes(data[offset : offset + 4])
            inventory.items.append(item)

            offset += 4

        return inventory

    def to_bytes(self) -> bytearray:
        """
        Converts the inventory to bytes.

        Returns
        -------
        bytearray
            The converted inventory.
        """

        data = bytearray(self.version.to_bytes(1, "little"))
        data += bytearray(self.slots.to_bytes(4, "little"))
        data += bytearray(self.item_count.to_bytes(2, "little"))

        for item in self.items:
            data += item.to_bytes()

        return data
