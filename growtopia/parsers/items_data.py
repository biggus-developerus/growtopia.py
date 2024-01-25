__all__ = (
    "ItemsData",
    "Item",
)

from dataclasses import (
    dataclass,
)
from time import time
from typing import Iterator, Union, Optional

from .enums import (
    ItemClothingType,
    ItemProperty,
    ItemCategory,
    ItemVisualEffectType,
    ItemCollisionType,
)

from ..constants import (
    IGNORED_ATTRS,
    ITEM_ATTR_SIZES,
)
from ..utils.ansi import (
    AnsiStr,
)
from ..utils.buffer import (
    ReadBuffer,
    WriteBuffer,
)
from ..utils.file import File
from ..utils.logger import (
    Logger,
    LogLevel,
)
from ..utils.proton import (
    decrypt,
    encrypt,
    proton_hash,
)


@dataclass
class Item:
    id: int = 0
    properties: ItemProperty = ItemProperty(0)
    category: ItemCategory = ItemCategory(0)
    material_type: int = 0  # TODO: find out what this shit is

    name: str = ""

    texture_path: str = ""
    texture_hash: int = 0

    visual_effect_type: ItemVisualEffectType = ItemVisualEffectType(0)

    flags2: int = 0  # TODO: find out what this shit is

    texture_x: int = 0
    texture_y: int = 0

    storage_type: int = 0  # TODO: find out what this shit is
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

    overlay_object: bytearray = None

    flags4: int = 0

    reserved: bytearray = None

    punch_options: str = ""

    flags5: int = 0
    bodypart: bytearray = None

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

    def set_texture_file(
        self,
        texture_path: str,
        file_path_or_data: Union[str, memoryview],
    ) -> None:
        if not isinstance(file_path_or_data, (str, memoryview)):
            raise TypeError(f"Expected str or memoryview, got {type(file_path_or_data)}")

        file = ReadBuffer.load(file_path_or_data)

        self.texture_path = texture_path
        self.texture_hash = proton_hash(file.data)

    def set_extra_file(
        self,
        extra_path: str,
        file_path_or_data: Union[str, memoryview],
    ) -> None:
        if not isinstance(file_path_or_data, (str, memoryview)):
            raise TypeError(f"Expected str or memoryview, got {type(file_path_or_data)}")

        file = ReadBuffer.load(file_path_or_data)

        self.extra_file_path = extra_path
        self.extra_file_hash = proton_hash(file.data)

    def to_bytes(self, version: int, write_buffer: WriteBuffer) -> WriteBuffer:
        for attr in self.__dict__:
            if attr in IGNORED_ATTRS.get(version, []):
                continue

            attr_value = getattr(self, attr)

            if isinstance(attr_value, int):
                write_buffer.write_int(attr_value, ITEM_ATTR_SIZES[attr])
            elif isinstance(attr_value, ItemProperty):
                write_buffer.write_int(attr_value.value, ITEM_ATTR_SIZES[attr])
            elif isinstance(attr_value, str):
                if attr == "name":
                    attr_value = encrypt(attr_value, self.id)

                data = bytearray([ord(char) for char in attr_value])

                write_buffer.write_int(len(data), 2)
                write_buffer.write_bytes(data)
            elif isinstance(attr_value, bytearray):
                write_buffer.write_bytes(attr_value)
            else:
                raise TypeError(f"Unknown attribute type: {type(attr_value)}")

        return write_buffer

    @property
    def is_foreground(self) -> bool:
        return self.category == ItemCategory.FOREGROUND

    @property
    def is_background(self) -> bool:
        return self.category == ItemCategory.BACKGROUND

    @property
    def is_weather_machine(self) -> bool:
        return (
            self.category == ItemCategory.WEATHER_MACHINE
            or self.category == ItemCategory.SPECIAL_WEATHER_MACHINE
            or self.category == ItemCategory.SPECIAL_WEATHER_MACHINE2
            or self.category == ItemCategory.INFINITY_WEATHER_MACHINE
        )

    @property
    def is_pain_block(self) -> bool:
        return (
            self.category == ItemCategory.PAIN_BLOCK
            or self.category == ItemCategory.ACID_PAIN_BLOCK
        )

    @property
    def is_deadly_block(self) -> bool:
        return (
            self.category == ItemCategory.SPIKE
            or self.category == ItemCategory.TOGGLEABLE_DEADLY_BLOCK
            or self.collision_type == ItemCategory.TOGGLEABLE_DEADLY_BLOCK
        )

    def __repr__(self) -> str:
        return f"<Item id={self.id} name={self.name}>"

    def __str__(self) -> str:
        return repr(self)

    def __post_init__(self):
        self.overlay_object = bytearray([0] * 8)
        self.reserved = bytearray([0] * 68)
        self.bodypart = bytearray([0] * 9)

    @classmethod
    def from_bytes(cls, version: int, buffer: ReadBuffer) -> "Item":
        item = cls()

        for attr in item.__dict__:
            if attr in IGNORED_ATTRS.get(version, []):
                continue

            attr_value = getattr(item, attr)

            if isinstance(attr_value, (int, ItemProperty)):
                setattr(item, attr, attr_value.__class__(buffer.read_int(ITEM_ATTR_SIZES[attr])))
            elif isinstance(attr_value, str):
                string = buffer.read_string()

                if attr == "name":
                    string = decrypt(string, item.id)

                setattr(item, attr, string)
            elif isinstance(attr_value, bytearray):
                setattr(item, attr, bytearray(buffer.read_bytes(ITEM_ATTR_SIZES[attr])))
            else:
                raise TypeError(f"Unknown attribute type: {type(attr_value)}")

        return item


class ItemsData(File):
    def __init__(self, pob: Optional[Union[str, memoryview]] = None) -> None:
        super().__init__()

        if pob and not isinstance(pob, (str, memoryview)):
            raise TypeError(f"Expected str, memoryview, or None, got {type(pob)}")

        if pob and not File.is_items_data(pob):
            raise ValueError("File is not items.dat")

        self.buffer: Union[ReadBuffer, WriteBuffer] = ReadBuffer.load(pob) if pob else WriteBuffer()

        self.version: int = 0
        self.hash: int = 0
        self.items: list[Item] = []

    def parse(self) -> bool:
        if not isinstance(self.buffer, (ReadBuffer, WriteBuffer)):
            raise TypeError(f"Expected ReadBuffer or WriteBuffer, got {type(self.buffer)}")

        if isinstance(self.buffer, WriteBuffer):
            self.buffer = ReadBuffer.load(self.buffer.data)

        self.hash = self._get_hash()

        self.version = self.buffer.read_int(2)
        item_count = (
            self.buffer.read_int()
        )  # no more self.items_count, grow up and use len(self.items)

        self.items = []

        progress = 0  # percentage
        timings = []

        start_time = time()

        if self.version not in IGNORED_ATTRS:
            Logger.log(
                f"Unknown item version, {self.version}, parsing might fail.",
                LogLevel.WARNING,
            )

        for i in range(0, item_count):
            item_start_time = time()
            item = Item.from_bytes(self.version, self.buffer)

            if i / item_count * 100 > progress + 10:
                Logger.log(
                    f"Parsing items.dat, {i / item_count * 100:.2f}%",
                    LogLevel.INFO,
                )
                progress += 10

            self.items.append(item)
            timings.append(time() - item_start_time)

        end = time() - start_time

        Logger.log_ansi(AnsiStr.clear())
        Logger.wait_until_flushed()
        Logger.log(
            f"Parsed items.dat (took {end*1_000:.0f}ms & average item/s {(sum(timings) / item_count) * (10**6):.0f}μs) {self}",
            LogLevel.INFO,
        )

        return True

    def serialise(self, overwrite_read_buff: bool = False) -> ReadBuffer:
        write_buffer = WriteBuffer()

        write_buffer.write_int(self.version, 2)
        write_buffer.write_int(len(self.items))

        if self.version not in IGNORED_ATTRS:
            Logger.log(
                f"Unknown item version, {self.version}, serialisation might fail.",
                LogLevel.WARNING,
            )

        progress = 0  # percentage
        timings = []

        start_time = time()

        for i, item in enumerate(self.items):
            if i != item.id:
                raise ValueError(f"Item ID mismatch, expected {i}, got {item.id} {item}")

            item_start_time = time()
            item.to_bytes(self.version, write_buffer)

            if (perc := i / len(self.items) * 100) > progress + 10:
                Logger.log(
                    f"Serialising items.dat, {perc:.2f}%",
                    LogLevel.INFO,
                )
                progress += 10

            timings.append(time() - item_start_time)

        read_buffer = ReadBuffer.load(write_buffer.data)

        if overwrite_read_buff:
            self.buffer = read_buffer

        end = time() - start_time

        Logger.log_ansi(AnsiStr.clear())
        Logger.wait_until_flushed()

        Logger.log(
            f"Serialised items.dat (took {end*1_000:.0f}ms & average item/s {(sum(timings) / len(self.items)) * (10**6):.0f}μs) {self}",
            LogLevel.INFO,
        )

        return read_buffer

    def save(self, path: str) -> None:
        self.serialise(True)  # overwrite read buffer (self.buffer)
        super().save(path)  # save file

    def add_item(self, item: Item, keep_id: bool = False) -> None:
        if item.id == 0 and not keep_id:
            item.id = len(self.items)

        self.items.append(item)

    def remove_item(self, item_id: int) -> None:
        self.items.pop(item_id)
        self.item_count -= 1

    def get_item(self, item_id: int) -> Item:
        return self.items[item_id]

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, index: int) -> Item:
        return self.get_item(index)

    def __setitem__(self, index: int, value: Item) -> None:
        if not isinstance(value, Item):
            raise TypeError(f"Expected Item, got {type(value)}")

        self.items[index] = value

    def __iter__(self) -> Iterator[Item]:
        return iter(self.items)

    def __repr__(self) -> str:
        return f"<ItemsData version={self.version} item_count={len(self.items)} hash={self.hash}>"

    def __str__(self) -> str:
        return repr(self)
