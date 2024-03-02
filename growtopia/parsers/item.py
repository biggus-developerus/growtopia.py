__all__ = ("Item",)

from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Callable,
    Dict,
    Type,
    TypeVar,
)

from ..utils import (
    Buffer,
    xor_cipher,
)
from .constants import *
from .enums import *
from .punch_options import *

T = TypeVar("T")


def deserialise_enum(t: Type[T], size: int, buffer: Buffer) -> T:
    return t(buffer.read_int(size))


# deal with it, daft monkey.

ITEM_DESERIALISERS: Dict[Type[T], Callable[[str, Buffer], T]] = {
    **{
        e_type: lambda attr, buffer, e_type=e_type: e_type(buffer.read_int(ITEM_ATTR_SIZES[attr]))
        for e_type in ITEM_ENUM_TYPES
    },
    int: lambda attr, buffer: buffer.read_int(ITEM_ATTR_SIZES[attr]),
    bool: lambda attr, buffer: bool(buffer.read_int(ITEM_ATTR_SIZES[attr])),
    str: lambda _, buffer: buffer.read_str(buffer.read_int(2)),
    bytearray: lambda attr, buffer: bytearray(buffer.read(ITEM_ATTR_SIZES[attr])),
    ItemPunchOptions: lambda _, buffer: ItemPunchOptions.from_str(
        buffer.read_str(buffer.read_int(2))
    ),
}

ITEM_SERIALISERS: Dict[Type[T], Callable[[str, T, Buffer], None]] = {
    **{
        e_type: lambda attr, value, buffer: buffer.write_int(value, ITEM_ATTR_SIZES[attr])
        for e_type in ITEM_ENUM_TYPES
    },
    int: lambda attr, value, buffer: buffer.write_int(value, ITEM_ATTR_SIZES[attr]),
    bool: lambda attr, value, buffer: buffer.write_int(int(value), ITEM_ATTR_SIZES[attr]),
    str: lambda _, value, buffer: [
        buffer.write_int(len(value.encode()), 2),
        buffer.write_str(value),
    ],
    bytearray: lambda _, value, buffer: buffer.write(value),
    ItemPunchOptions: lambda _, value, buffer: [
        buffer.write_int(len((str_val := str(value)).encode()), 2),
        buffer.write_str(str_val),
    ],
}


@dataclass
class Item:
    id: int = 0

    properties: ItemProperty = ItemProperty(0)
    category: ItemCategory = ItemCategory(0)
    material_type: ItemMaterialType = ItemMaterialType(0)

    name: str = ""

    texture_path: str = ""
    texture_hash: int = 0

    visual_effect_type: ItemVisualEffectType = ItemVisualEffectType(0)

    flags2: int = 0  # TODO: find out what this shit is

    texture_x: int = 0
    texture_y: int = 0

    storage_type: ItemStorageType = ItemStorageType(0)
    is_stripey_wallpaper: int = 0
    collision_type: ItemCollisionType = ItemCollisionType(0)
    break_hits: int = 0

    reset_time: int = 0

    clothing_type: ItemClothingType = ItemClothingType(0)
    rarity: int = 0
    max_amount: int = 0

    extra_file_path: str = ""
    extra_file_hash: int = 0

    audio_volume: int = 0

    pet_name: str = ""
    pet_prefix: str = ""
    pet_suffix: str = ""
    pet_ability: str = ""

    seed_base_index: int = 0
    seed_overlay_index: int = 0
    tree_base_index: int = 0
    tree_leaves_index: int = 0
    seed_colour: int = 0
    seed_overlay_colour: int = 0

    ingredient: int = 0

    grow_time: int = 0

    flags3: int = 0
    is_rayman: int = 0

    extra_options: str = ""
    texture_path2: str = ""
    extra_options2: str = ""

    overlay_object: bytearray = field(default_factory=bytearray)

    flags4: int = 0

    reserved: bytearray = field(default_factory=bytearray)

    punch_options: ItemPunchOptions = ItemPunchOptions()

    flags5: int = 0
    bodypart: bytearray = field(default_factory=bytearray)

    flags6: int = 0

    growpass_property: int = 0

    can_player_sit: bool = False
    sit_player_offset_x: int = 0
    sit_player_offset_y: int = 0
    sit_overlay_x: int = 0
    sit_overlay_y: int = 0
    sit_overlay_offset_x: int = 0
    sit_overlay_offset_y: int = 0
    sit_overlay_texture: str = ""

    renderer_file_path: str = ""

    @staticmethod
    def from_bytes(data: Buffer, version) -> "Item":
        item = Item()

        for attr in item.__dict__:
            if attr in ITEM_IGNORED_ATTRS[version]:
                continue

            ret = ITEM_DESERIALISERS[type(getattr(item, attr))](attr, data)
            setattr(item, attr, ret)

            if attr == "name":
                item.name = xor_cipher(item.name, item.id)

        return item

    def to_bytes(self, buffer: Buffer, version: int) -> None:
        for attr in self.__dict__:
            if attr in ITEM_IGNORED_ATTRS[version]:
                continue

            if attr == "name":
                buffer.write_int(len((name := xor_cipher(self.name, self.id)).encode()), 2)
                buffer.write_str(name)

                continue

            ITEM_SERIALISERS[type(getattr(self, attr))](attr, getattr(self, attr), buffer)

    def is_of_category(self, item_category: ItemCategory) -> bool:
        return self.category == item_category

    def has_property(self, item_property: ItemProperty) -> bool:
        return self.properties & item_property

    @property
    def is_flippable(self) -> bool:
        return bool(self.properties & ItemProperty.FLIPPABLE)

    @property
    def is_editable(self) -> bool:
        return bool(self.properties & ItemProperty.EDITABLE)

    @property
    def is_seedless(self) -> bool:
        return bool(self.properties & ItemProperty.SEEDLESS)

    @property
    def is_permanent(self) -> bool:
        return bool(self.properties & ItemProperty.PERMANENT)

    @property
    def is_dropless(self) -> bool:
        return bool(self.properties & ItemProperty.DROPLESS)

    @property
    def has_shadow(self) -> bool:
        return not self.properties & ItemProperty.NO_SHADOW

    @property
    def is_lock(self) -> bool:
        return bool(self.properties & ItemProperty.LOCK)

    @property
    def is_in_beta(self) -> bool:
        return bool(self.properties & ItemProperty.BETA)

    @property
    def is_auto_pickup(self) -> bool:
        return bool(self.properties & ItemProperty.AUTO_PICKUP)

    @property
    def is_mod_only_item(self) -> bool:
        return bool(self.properties & ItemProperty.MOD)

    @property
    def grows_randomly(self) -> bool:
        return bool(self.properties & ItemProperty.RAND_GROW)

    @property
    def is_public(self) -> bool:
        return bool(self.properties & ItemProperty.PUBLIC)

    @property
    def is_foreground(self) -> bool:
        return bool(self.properties & ItemProperty.FOREGROUND)

    @property
    def is_holiday_item(self) -> bool:
        return bool(self.properties & ItemProperty.HOLIDAY)

    @property
    def is_untradeable(self) -> bool:
        return bool(self.properties & ItemProperty.UNTRADEABLE)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: name={self.name}, id={self.id}, properties={self.properties}>"
