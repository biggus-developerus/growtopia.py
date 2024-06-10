__all__ = (
    "ITEM_IGNORED_ATTRS",
    "ITEM_ATTR_SIZES",
    "ITEM_ENUM_TYPES",
    "LATEST_ITEMS_DATA_VERSION",
)

from typing import (
    Dict,
    List,
    Type,
)

from .enums import *

LATEST_ITEMS_DATA_VERSION: int = 18

ITEM_ATTR_SIZES: Dict[str, int] = {
    "id": 4,
    "properties": 2,
    "category": 1,
    "material_type": 1,
    "texture_hash": 4,
    "visual_effect_type": 1,
    "flags2": 4,
    "storage_type": 1,
    "is_stripey_wallpaper": 1,
    "collision_type": 1,
    "break_hits": 1,
    "reset_time": 4,
    "clothing_type": 1,
    "rarity": 2,
    "max_amount": 1,
    "extra_file_hash": 4,
    "audio_volume": 4,
    "ingredient": 4,
    "grow_time": 4,
    "flags3": 2,
    "is_rayman": 2,
    "overlay_object": 8,
    "flags4": 4,
    "reserved": 68,
    "flags5": 4,
    "bodypart": 9,
    "flags6": 4,
    "growpass_property": 4,
    "unknown_int": 4,
    "renderer_file_hash": 4,
}

# TODO: Support older versions
ITEM_IGNORED_ATTRS: Dict[int, List[str]] = {
    17: ["renderer_file_hash"],
    18: [],
}

ITEM_ENUM_TYPES: List[Type] = [
    ItemProperty,
    ItemCategory,
    ItemMaterialType,
    ItemVisualEffectType,
    ItemStorageType,
    ItemCollisionType,
    ItemClothingType,
]
