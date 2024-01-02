__all__ = ("Tile",)

import asyncio

from ..item import Item
from ..obj_holder import ObjHolder
from ..protocol import GameUpdatePacket, GameUpdatePacketFlags, GameUpdatePacketType
from .tile_extra import TileExtra


class Tile(TileExtra):
    def __init__(
        self, *, foreground: Item | None = None, background: Item | None = None, pos: tuple[int, int] = (0, 0)
    ) -> None:
        super().__init__()

        self.foreground_id: int = foreground.id if type(foreground) == None else 0
        self.background_id: int = background.id if type(background) == None else 0

        self.lockpos: int = 0
        self.flags: int = 0

        self.label: str = ""

        self.pos: tuple[int, int] = pos

        self._damage_dealt_to_foreground: int = 0
        self._damage_dealt_to_background: int = 0

    def set_item(self, item: Item, **kwargs) -> None:
        """
        Sets the foreground/background item.

        Parameters
        ----------
        item: Item
            The item to set.
        **kwargs: dict
            Depending on the item passed in, this may be required.
            If you're passing in something like a main door, you'd need to pass in the door_label. (defaults to an empty str)
        """
        self.foreground = item if item.is_foreground else self.foreground
        self.background = item if item.is_background else self.background
        self.label = kwargs["door_label"] if "door_label" in list(kwargs.keys()) else self.label

        match item.action_type:
            case 13:
                self.flags = 1
                self._set_door_extra_data(self.label)

    async def _start_reset_timer(
        self,
        damage_applied_to: Item,
    ) -> None:
        await asyncio.sleep(self.item.reset_time)

        if self.is_empty or self.health <= 0 or self.item != damage_applied_to:
            return

        self.reset_damage_dealt_to_layer()

    def punch(self, damage: int = 1, reset: bool = True) -> bool:
        """
        Punches the tile.

        Parameters
        ----------
        damage: int
            The amount of damage to deal to the tile.
        reset: bool
            Whether or not to reset the damage dealt to the tile after a certain amount of time.

        Returns
        -------
        bool:
            True if the tile was punched, False otherwise.
        """
        if self.is_empty:
            return False

        self.deal_damage_to_layer(damage)

        if reset:
            asyncio.create_task(self._start_reset_timer(self.item))

        return True

    def break_layer(self) -> None:
        """
        Breaks a layer. If the foreground item is not blank, it will be broken, otherwise the background item will be broken.
        "Broken" means the layer will be set to blank.
        """

        BLANK: Item = ObjHolder.items_data.get_item(0)

        if self.foreground != 0:
            self.foreground = BLANK
            self._damage_dealt_to_foreground = 0
            return

        if self.background != 0:
            self.background = BLANK
            self._damage_dealt_to_background = 0
            return

    def get_layer(self) -> Item:
        """
        Gets the layer. If the foreground item is not blank, it will be returned, otherwise the background item will be returned.

        Returns
        -------
        Item:
            The current layer.
        """
        return self.foreground if self.foreground != 0 else self.background

    def deal_damage_to_layer(self, damage: int) -> None:
        """
        Deals damage to the layer. If the foreground item is not blank, it will be dealt to, otherwise the background item will be dealt to.

        Parameters
        ----------
        damage: int
            The amount of damage to deal to the layer.
        """

        if self.is_empty:
            return

        if self.foreground != 0:
            self._damage_dealt_to_foreground += damage
            return

        self._damage_dealt_to_background += damage

    def reset_damage_dealt_to_layer(self) -> None:
        """
        Resets the damage dealt to the layer. If the foreground item is not blank, it will be reset, otherwise the background item will be reset.
        """

        if self.is_empty:
            return

        if self.foreground != 0:
            self._damage_dealt_to_foreground = 0
            return

        self._damage_dealt_to_background = 0

    def apply_damage_packet(self, net_id: int, tile_damage: int = 6) -> GameUpdatePacket:
        return GameUpdatePacket(
            update_type=GameUpdatePacketType.TILE_APPLY_DAMAGE,
            int_x=self.pos[0],
            int_y=self.pos[1],
            int_=tile_damage,
            net_id=net_id,
            extra_data=b"\x00",
        )

    @property
    def health(self) -> int:
        """
        The health of the tile.
        """
        if self.is_empty:
            return 0

        return self.get_layer().break_hits - self.damage_dealt

    @property
    def damage_dealt(self) -> int:
        """
        The damage dealt to the tile.
        """
        if self.is_empty:
            return 0

        if self.foreground != 0:
            return self._damage_dealt_to_foreground

        return self._damage_dealt_to_background

    @property
    def is_empty(self) -> bool:
        """
        Whether or not the tile is empty.
        """
        return self.foreground.id == 0 and self.background.id == 0

    @property
    def update_packet(self) -> GameUpdatePacket:
        return GameUpdatePacket(
            update_type=GameUpdatePacketType.SEND_TILE_UPDATE_DATA,
            flags=GameUpdatePacketFlags.EXTRA_DATA,
            int_x=self.pos[0],
            int_y=self.pos[1],
            extra_data=self.serialise(),
        )

    @property
    def item(self) -> Item:
        """
        The foreground/background item. If the foreground item is not blank, it will be returned, otherwise the background item will be returned.
        """
        return self.foreground if self.foreground != 0 else self.background

    @property
    def foreground(self) -> Item:
        """
        The foreground item.
        """

        return ObjHolder.items_data.get_item(self.foreground_id)

    @property
    def background(self) -> Item:
        """
        The background item.
        """
        return ObjHolder.items_data.get_item(self.background_id)

    @foreground.setter
    def foreground(self, item: Item) -> None:
        self.foreground_id = item.id

        if self.foreground_id == 0 and self.item.is_foreground:
            self.flags = 0
            self.reset_extra_data()

    @background.setter
    def background(self, item: Item) -> None:
        self.background_id = item.id

        if self.background_id == 0 and self.item.is_background:
            self.flags = 0
            self.reset_extra_data()

    def serialise(self) -> bytearray:
        """
        Serialises the tile.

        Returns
        -------
        bytearray:
            The serialised world.
        """
        data = bytearray()

        data += self.foreground_id.to_bytes(2, "little")
        data += self.background_id.to_bytes(2, "little")

        data += self.lockpos.to_bytes(2, "little")
        data += self.flags.to_bytes(2, "little")

        data += self._serialise_extra_data()

        return data

    @classmethod
    def from_bytes(cls, data: bytes) -> "Tile":
        """
        Creates a tile from bytes.

        Parameters
        ----------
        data: bytes
            The bytes to create the tile from.

        Returns
        -------
        Tile:
            The tile.
        """
        tile = cls()

        tile.foreground = int.from_bytes(data[:2], "little")
        tile.background = int.from_bytes(data[2:4], "little")

        tile.lockpos = int.from_bytes(data[4:6], "little")
        tile.flags = int.from_bytes(data[6:8], "little")

        if tile.flags != 0:  # TODO: Obviously handle the extra data.. 😢
            tile.extra_data_type = int.from_bytes(data[8:9], "little")
            tile.extra_data = data[9:]

        return tile
