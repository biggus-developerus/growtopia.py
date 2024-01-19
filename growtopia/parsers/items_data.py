__all__ = (
    "ItemsData",
    "Item",
)

from dataclasses import (
    dataclass
)
from typing import (
    Iterator,
    Union
)

from ..constants import (
    IGNORED_ATTRS,
    ITEM_ATTR_SIZES
)
from ..utils import (
    File,
    ReadBuffer,
    WriteBuffer,
    decrypt,
    encrypt,
    proton_hash
)


@dataclass
class Item:
    id: int = 0

    editable_type: int = 0
    category: int = 0
    action_type: int = 0
    hit_sound_type: int = 0

    name: str = ""
    texture: str = ""

    texture_hash: int = 0
    kind: int = 0

    flags1: int = 0
    texture_x: int = 0
    texture_y: int = 0

    spread_type: int = 0
    is_stripey_wallpaper: int = 0
    collision_type: int = 0

    break_hits: int = 0

    reset_time: int = 0
    clothing_type: int = 0
    rarity: int = 0

    max_amount: int = 0

    extra_file: str = ""
    extra_file_hash: int = 0
    audio_volume: int = 0

    pet_name: str = ""
    pet_prefix: str = ""
    pet_suffix: str = ""
    pet_ability: str = ""

    seed_base: int = 0
    seed_overlay: int = 0
    tree_base: int = 0
    tree_leaves: int = 0

    seed_colour: int = 0
    seed_overlay_colour: int = 0

    ingredient: int = 0
    grow_time: int = 0

    flags2: int = 0
    rayman: int = 0

    extra_options: str = ""
    texture2: str = ""
    extra_options2: str = ""

    reserved: Union[bytearray, None] = None

    punch_options: str = ""

    flags3: int = 0
    bodypart: Union[bytearray, None] = None
    flags4: int = 0
    flags5: int = 0
    unknown: Union[bytearray, None] = None
    sit_file: str = ""

    renderer_file: str = ""

    def set_texture_file(
        self,
        texture_path: str,
        file_path_or_data: Union[str, memoryview],
    ) -> None:
        if not isinstance(file_path_or_data, (str, memoryview)):
            raise TypeError(f"Expected str or memoryview, got {type(file_path_or_data)}")

        file = ReadBuffer.load(file_path_or_data)

        self.texture = texture_path
        self.texture_hash = proton_hash(file.data)

    def set_extra_file(
        self,
        extra_path: str,
        file_path_or_data: Union[str, memoryview],
    ) -> None:
        if not isinstance(file_path_or_data, (str, memoryview)):
            raise TypeError(f"Expected str or memoryview, got {type(file_path_or_data)}")

        file = ReadBuffer.load(file_path_or_data)

        self.extra_file = extra_path
        self.extra_file_hash = proton_hash(file.data)

    def __repr__(self) -> str:
        return f"<Item id={self.id} name={self.name}>"

    def __str__(self) -> str:
        return repr(self)

    def __post_init__(self):
        self.reserved = bytearray([0] * 80)
        self.bodypart = bytearray([0] * 9)
        self.unknown = bytearray([0] * 25)


class ItemsData(File):
    def __init__(self, path_or_data: Union[str, bytes, bytearray]) -> None:
        if not isinstance(path_or_data, (str, bytes, bytearray)):
            raise TypeError(f"Expected str, bytes or bytearray, got {type(path_or_data)}")

        if isinstance(path_or_data, (bytes, bytearray)):
            path_or_data = memoryview(path_or_data)

        if not File.is_items_data(path_or_data):
            raise ValueError("File is not items.dat")

        self.buffer: ReadBuffer = ReadBuffer.load_file(path_or_data)

        self.version: int = 0
        self.item_count: int = 0
        self.hash: int = 0

        self.items: list[Item] = []

    def parse(self) -> None:
        self.hash = self._get_hash()

        self.version = self.buffer.read_int(2)
        self.item_count = self.buffer.read_int()
        self.items = []

        for i in range(0, self.item_count):
            item = Item()

            for attr in item.__dict__:
                if attr in IGNORED_ATTRS.get(self.version, []):
                    continue

                attr_value = getattr(item, attr)

                if isinstance(attr_value, int):
                    setattr(item, attr, self.buffer.read_int(ITEM_ATTR_SIZES[attr]))
                elif isinstance(attr_value, str):
                    string = self.buffer.read_string()

                    if attr == "name":
                        string = decrypt(string, item.id)

                    setattr(item, attr, string)
                elif isinstance(attr_value, bytearray):
                    setattr(item, attr, bytearray(self.buffer.read_bytes(ITEM_ATTR_SIZES[attr])))
                else:
                    raise TypeError(f"Unknown attribute type: {type(attr_value)}")

            if item.id != i:
                raise ValueError(f"Item ID mismatch, expected {i}, got {item.id} {item}")

            self.items.append(item)

    def serialise(self, overwrite_read_buff: bool = False) -> ReadBuffer:
        write_buffer = WriteBuffer()

        write_buffer.write_int(self.version, 2)
        write_buffer.write_int(self.item_count)

        for i, item in enumerate(self.items):
            if i != item.id:
                raise ValueError("Item ID mismatch")

            for attr in item.__dict__:
                if attr in IGNORED_ATTRS.get(self.version, []):
                    continue

                attr_value = getattr(item, attr)

                if isinstance(attr_value, int):
                    write_buffer.write_int(attr_value, ITEM_ATTR_SIZES[attr])
                elif isinstance(attr_value, str):
                    if attr == "name":
                        attr_value = encrypt(attr_value, item.id)

                    data = bytearray([ord(char) for char in attr_value])

                    write_buffer.write_int(len(data), 2)
                    write_buffer.write_bytes(data)
                elif isinstance(attr_value, bytearray):
                    write_buffer.write_bytes(attr_value)
                else:
                    raise TypeError(f"Unknown attribute type: {type(attr_value)}")

        read_buffer = ReadBuffer.load(write_buffer.data)

        if overwrite_read_buff:
            self.buffer = read_buffer

        return read_buffer

    def save(self, path: str) -> None:
        self.serialise(True)  # overwrite read buffer (self.buffer)
        super().save(path)  # save file

    def add_item(self, item: Item, keep_id: bool = False) -> None:
        if item.id == 0 and not keep_id:
            item.id = self.item_count

        self.items.append(item)
        self.item_count += 1

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
        return f"<ItemsData version={self.version} item_count={self.item_count} hash={self.hash}>"

    def __str__(self) -> str:
        return repr(self)
