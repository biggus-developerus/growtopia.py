__all__ = ("Item",)

from typing import Any


# TODO: Add docstring to the Item class
class Item:
    def __init__(self) -> None:
        self.id: int = 4

        self.editable_type: int = 1
        self.category: int = 1
        self.action_type: int = 1
        self.hit_sound_type: int = 1

        self.name: str = ""
        self.texture: str = ""

        self.texture_hash: int = 4
        self.kind: int = 1

        self.flags1: int = 4
        self.texture_x: int = 1
        self.texture_y: int = 1

        self.spread_type: int = 1
        self.is_stripey_wallpaper: int = 1
        self.collision_type: int = 1

        self.break_hits: int = 1

        self.reset_time: int = 4
        self.clothing_type: int = 1
        self.rarity: int = 2

        self.max_amount: int = 1

        self.extra_file: str = ""
        self.extra_file_hash: int = 4
        self.audio_volume: int = 4

        self.pet_name: str = ""
        self.pet_prefix: str = ""
        self.pet_suffix: str = ""
        self.pet_ability: str = ""

        self.seed_base: int = 1
        self.seed_overlay: int = 1
        self.tree_base: int = 1
        self.tree_leaves: int = 1

        self.seed_colour: int = 4
        self.seed_overlay_colour: int = 4

        self.ingredient: int = 4
        self.grow_time: int = 4

        self.flags2: int = 2
        self.rayman: int = 2

        self.extra_options: str = ""
        self.texture2: str = ""
        self.extra_options2: str = ""

        self.reserved: bytearray = bytearray(80)

        self.punch_options: str = ""

        self.flags3: int = 4
        self.bodypart: bytearray = bytearray(9)
        self.flags4: int = 4
        self.flags5: int = 4
        self.unknown: bytearray = bytearray(25)
        self.sit_file: str = ""

    @property
    def is_foreground(self) -> bool:
        return self.action_type != 18

    @property
    def is_background(self) -> bool:
        return self.action_type == 18

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Item):
            return self.id == other.id
        if isinstance(other, int):
            return self.id == other
        if isinstance(other, str):
            return self.name == other

        return False

    def __str__(self) -> str:
        return f"{self.name} ({self.id})"
