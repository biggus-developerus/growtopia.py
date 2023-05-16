__all__ = (
    "PacketType",
    "VariantType",
    "GameUpdatePacketFlags",
    "GameUpdatePacketType",
)

from enum import IntEnum


class PacketType(IntEnum):
    """
    An integer enumeration of all packet types.
    """

    UNKNOWN = 0
    HELLO = 1
    TEXT = 2
    GAME_MESSAGE = 3
    GAME_UPDATE = 4

    @classmethod
    def _missing_(cls, _: int) -> "PacketType":
        return cls(0)


class VariantType(IntEnum):
    NONE = 0
    FLOAT = 1
    STR = 2
    VECTOR2 = 3
    VECTOR3 = 4
    UINT = 8
    INT = 9

    # Custom variant types. Not related to Growtopia.
    DIALOG = 10

    @classmethod
    def _missing_(cls, _):
        return cls.NONE


class GameUpdatePacketFlags(IntEnum):
    UNKNOWN = -1
    EXTRA_DATA = 8

    @classmethod
    def _missing_(cls, _):
        return cls.UNKNOWN


class GameUpdatePacketType(IntEnum):
    UNKNOWN = -1
    STATE = 0
    CALL_FUNCTION = 1
    UPDATE_STATUS = 2
    TILE_CHANGE_REQUEST = 3
    SEND_MAP_DATA = 4
    SEND_TILE_UPDATE_DATA = 5
    SEND_TILE_UPDATE_DATA_MULTIPLE = 6
    TILE_ACTIVATE_REQUEST = 7
    TILE_APPLY_DAMAGE = 8
    SEND_INVENTORY_STATE = 9
    ITEM_ACTIVATE_REQUEST = 10
    ITEM_ACTIVATE_OBJECT_REQUEST = 11
    SEND_TILE_TREE_STATE = 12
    MODIFY_ITEM_INVENTORY = 13
    ITEM_CHANGE_OBJECT = 14
    SEND_LOCK = 15
    SEND_ITEM_DATABASE_DATA = 16
    SEND_PARTICLE_EFFECT = 17
    SET_ICON_STATE = 18
    ITEM_EFFECT = 19
    SET_CHARACTER_STATE = 20
    PING_REPLY = 21
    PING_REQUEST = 22
    GOT_PUNCHED = 23
    APP_CHECK_RESPONSE = 24
    APP_INTEGRITY_FAIL = 25
    DISCONNECT = 26
    BATTLE_JOIN = 27
    BATTLE_EVENT = 28
    USE_DOOR = 29
    SEND_PARENTAL = 30
    GONE_FISHIN = 31
    STEAM = 32
    PET_BATTLE = 33
    NPC = 34
    SPECIAL = 35
    SEND_PARTICLE_EFFECT_V2 = 36
    ACTIVE_ARROW_TO_ITEM = 37
    SELECT_TILE_INDEX = 38
    SEND_PLAYER_TRIBUTE_DATA = 39

    @classmethod
    def _missing_(cls, _):
        return cls.UNKNOWN
