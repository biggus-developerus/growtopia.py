__all__ = ("Item",)

from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Callable,
    Dict,
    Optional,
    Type,
    TypeVar,
)

from ..net import HTTP
from ..utils import (
    Buffer,
    xor_cipher,
)
from .constants import *
from .enums import *
from .pet_info import *
from .punch_options import *
from .seed_info import *
from .sit_info import *

T = TypeVar("T")

# COPE + MALD + SEETHE

ITEM_DESERIALISERS: Dict[Type[T], Callable[[str, Buffer], T]] = {
    **{
        e_type: lambda attr, buffer, e_type=e_type: e_type(buffer.read_int(ITEM_ATTR_SIZES[attr]))
        for e_type in ITEM_ENUM_TYPES
    },
    int: lambda attr, buffer: buffer.read_int(ITEM_ATTR_SIZES[attr]),
    bool: lambda attr, buffer: bool(buffer.read_int(ITEM_ATTR_SIZES[attr])),
    str: lambda _, buffer: buffer.read_str(buffer.read_int(2)),
    bytearray: lambda attr, buffer: bytearray(buffer.read(ITEM_ATTR_SIZES[attr])),
    tuple: lambda _, buffer: (buffer.read_int(1), buffer.read_int(1)),
    ItemPetInfo: lambda _, buffer: ItemPetInfo.from_bytes(buffer),
    ItemSeedInfo: lambda _, buffer: ItemSeedInfo.from_bytes(buffer),
    ItemPunchOptions: lambda _, buffer: ItemPunchOptions.from_str(
        buffer.read_str(buffer.read_int(2))
    ),
    ItemSitInfo: lambda _, buffer: ItemSitInfo.from_bytes(buffer),
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
    tuple: lambda _, value, buffer: [buffer.write_int(value[0], 1), buffer.write_int(value[1], 1)],
    ItemPetInfo: lambda _, value, buffer: value.to_bytes(buffer),
    ItemSeedInfo: lambda _, value, buffer: value.to_bytes(buffer),
    ItemPunchOptions: lambda _, value, buffer: [
        buffer.write_int(len((str_val := str(value)).encode()), 2),
        buffer.write_str(str_val),
    ],
    ItemSitInfo: lambda _, value, buffer: value.to_bytes(buffer),
}


@dataclass
class ItemTextureInfo:
    path: str = ""
    hash: int = 0
    pos: tuple[int, int] = (0, 0)


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

    texture_pos: tuple[int, int] = (0, 0)

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

    pet_info: ItemPetInfo = field(default_factory=ItemPetInfo)
    seed_info: ItemSeedInfo = field(default_factory=ItemSeedInfo)

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

    punch_options: ItemPunchOptions = field(default_factory=ItemPunchOptions)
    
    flags5: int = 0
    bodypart: bytearray = field(default_factory=bytearray)

    flags6: int = 0

    growpass_property: int = 0

    sit_info: ItemSitInfo = field(default_factory=ItemSitInfo)

    renderer_file_path: str = ""

    @staticmethod
    def from_bytes(data: Buffer, version) -> "Item":
        item = Item()

        for attr in item.__dict__:
            if attr in ITEM_IGNORED_ATTRS[version]:
                continue

            setattr(item, attr, ITEM_DESERIALISERS[type(getattr(item, attr))](attr, data))

            if attr == "name":
                item.name = xor_cipher(item.name, item.id)
            elif attr == "break_hits":
                item.break_hits = item.break_hits // 6

        return item

    def to_bytes(self, buffer: Buffer, version: int) -> None:
        for attr in self.__dict__:
            if attr in ITEM_IGNORED_ATTRS[version]:
                continue

            attr_val = getattr(self, attr)

            if attr == "name":
                attr_val = xor_cipher(attr_val, self.id)
            elif attr == "break_hits":
                attr_val *= 6

            ITEM_SERIALISERS[type(attr_val)](attr, attr_val, buffer)

    def is_of_category(self, item_category: ItemCategory) -> bool:
        return self.category == item_category

    def has_property(self, item_property: ItemProperty) -> bool:
        return self.properties & item_property

    async def fetch_texture_file(self, **kwargs) -> Buffer:
        if not self.texture_path:
            return Buffer()

        return await HTTP.fetch_file_from_cdn(self.texture_path, **kwargs)

    async def fetch_texture_file2(self, **kwargs) -> Buffer:
        if not self.texture_path2:
            return Buffer()

        return await HTTP.fetch_file_from_cdn(self.texture_path2, **kwargs)

    async def fetch_extra_file(self, **kwargs) -> Buffer:
        if not self.extra_file_path:
            return Buffer()

        return await HTTP.fetch_file_from_cdn(self.extra_file_path, **kwargs)

    async def update_texture_hash(
        self,
        file_path: str = "",
        *,
        texture_hash: Optional[int] = None,
        **kwargs,
    ) -> bool:
        if texture_hash:
            self.texture_hash = texture_hash
            return True

        data: Buffer
        if not file_path:
            data = await self.fetch_texture_file(**kwargs)
        else:
            data = Buffer.load(file_path)

        if not data:
            return False

        self.texture_hash = data.hash()
        return True

    async def update_texture_hash2(
        self,
        file_path: str = "",
        *,
        texture_hash: Optional[int] = None,
        **kwargs,
    ) -> bool:
        if texture_hash:
            self.texture_hash = texture_hash
            return True

        data: Buffer
        if not file_path:
            data = await self.fetch_texture_file2(**kwargs)
        else:
            data = Buffer.load(file_path)

        if not data:
            return False

        self.texture_hash = data.hash()
        return True

    async def update_extra_file_hash(
        self,
        file_path: str = "",
        *,
        extra_file_hash: Optional[int] = None,
        **kwargs,
    ) -> bool:
        if extra_file_hash:
            self.extra_file_hash = extra_file_hash
            return True

        data: Buffer
        if not file_path:
            data = await self.fetch_extra_file(**kwargs)
        else:
            data = Buffer.load(file_path)

        if not data:
            return False

        self.extra_file_hash = data.hash()
        return True

    @property
    def texture_info(self) -> ItemTextureInfo:
        return ItemTextureInfo(
            self.texture_path,
            self.texture_hash,
            (self.texture_x, self.texture_y),
        )

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

    @property
    def is_clothing(self) -> bool:
        return self.category == ItemCategory.CLOTHING

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: name={self.name}, id={self.id}, category={self.category.name}, properties={self.properties.name}>"
