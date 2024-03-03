__all__ = (
    "ITEM_IGNORED_ATTRS",
    "ITEM_ATTR_SIZES",
    "ITEM_ENUM_TYPES",
)

from typing import (
    Dict,
    List,
    Type,
)

from .enums import *

ITEM_ATTR_SIZES: Dict[str, int] = {
    "id": 4,
    "properties": 2,
    "category": 1,
    "material_type": 1,
    "texture_hash": 4,
    "visual_effect_type": 1,
    "flags2": 4,
    "texture_x": 1,
    "texture_y": 1,
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
    "seed_base_index": 1,
    "seed_overlay_index": 1,
    "tree_base_index": 1,
    "tree_leaves_index": 1,
    "seed_colour": 4,
    "seed_overlay_colour": 4,
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
    "can_player_sit": 1,
    "sit_player_offset_x": 4,
    "sit_player_offset_y": 4,
    "sit_overlay_x": 4,
    "sit_overlay_y": 4,
    "sit_overlay_offset_x": 4,
    "sit_overlay_offset_y": 4,
}

ITEM_IGNORED_ATTRS: Dict[int, List[str]] = {
    11: [
        "flags5",
        "bodypart",
        "flags6",
        "growpass_property",
        "can_player_sit",
        "sit_player_offset_x",
        "sit_player_offset_y",
        "sit_overlay_x",
        "sit_overlay_y",
        "sit_overlay_offset_x",
        "sit_overlay_offset_y",
        "sit_overlay_texture",
        "renderer_file",
    ],
    12: [
        "flags4",
        "flags5",
        "unknown",
        "sit_file",
        "renderer_file",
    ],
    13: [
        "flags5",
        "unknown",
        "sit_file",
        "renderer_file",
    ],
    14: [
        "unknown",
        "sit_file",
        "renderer_file",
    ],
    15: [
        "renderer_file",
    ],
    16: [],
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
