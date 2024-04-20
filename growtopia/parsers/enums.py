__all__ = (
    "ItemClothingType",
    "ItemCategory",
    "ItemProperty",
    "ItemVisualEffectType",
    "ItemCollisionType",
    "ItemStorageType",
    "ItemMaterialType",
)

from typing import TypeVar

from aenum import (
    IntEnum,
    IntFlag,
)

from growtopia.utils import (
    LOG_LEVEL_WARNING,
    log,
)

T = TypeVar("T")


def _create_pseudo_member(cls: T, value: int) -> T:
    member_name = f"UNKNOWN_{value}"

    if member_name not in cls.__members__:
        member = int.__new__(cls, value)

        setattr(member, "_name_", member_name)
        setattr(member, "_value_", value)

        cls._value2member_map_[value] = member
        cls.__members__[member_name] = member

    return cls(value)


class IntEnumBase(IntEnum):
    @classmethod
    def _missing_(cls: T, value: int) -> T:
        log(LOG_LEVEL_WARNING, f"Unknown {cls.__name__} ({value}), returning pseudo member")
        return _create_pseudo_member(cls, value)


class ItemClothingType(IntEnumBase):
    HEAD = 0
    SHIRT = 1
    PANTS = 2
    FEET = 3
    FACE = 4
    HAND = 5
    BACK = 6
    HAIR = 7
    NECK = 8


class ItemCategory(IntEnumBase):
    FIST = 0
    WRENCH = 1
    DOOR = 2
    LOCK = 3
    GEMS = 4
    TREASURE = 5
    SPIKE = 6
    TRAMPOLINE = 7
    CONSUMABLE = 8
    ENTRANCE = 9
    SIGN = 10
    SFX_BLOCK = 11
    TOGGLEABLE_ANIMATED_BLOCK = 12
    MAIN_DOOR = 13
    PLATFORM = 14
    BEDROCK = 15
    LAVA = 16
    FOREGROUND = 17
    BACKGROUND = 18
    SEED = 19
    CLOTHING = 20
    ANIMATED_BLOCK = 21
    SFX_WALLPAPER = 22
    TOGGLEABLE_WALLPAPER = 23
    BOUNCY_BLOCK = 24
    PAIN_BLOCK = 25
    PORTAL = 26
    CHECKPOINT = 27
    SHEET_MUSIC = 28
    SLIPPERY_BLOCK = 29
    # UNKNOWN1 = 30
    TOGGLEABLE_BLOCK = 31
    CHEST = 32
    MAILBOX = 33
    BULLETIN_BOARD = 34
    EVENT_MYSTERY_BLOCK = 35
    RANDOM_BLOCK = 36
    COMPONENT = 37
    PROVIDER = 38
    CHEMICAL_COMBINER = 39
    ACHIEVEMENT_BLOCK = 40
    WEATHER_MACHINE = 41
    SCOREBOARD = 42
    SUNGATE = 43
    INTERNAL = 44
    TOGGLEABLE_DEADLY_BLOCK = 45
    HEART_MONITOR = 46
    DONATION_BOX = 47
    # UNKNOWN2 = 48
    MANNEQUIN = 49
    SECURITY_CAMERA = 50
    MAGIC_EGG = 51
    GAME_BLOCK = 52
    GAME_GENERATOR = 53
    XENONITE_CRYSTAL = 54
    PHONE_BOOTH = 55
    CRYSTAL = 56
    CRIME_IN_PROGRESS = 57
    CLOTHING_COMPACTOR = 58
    SPOTLIGHT = 59
    PUSHING_BLOCK = 60
    DISPLAY_BLOCK = 61
    VENDING_MACHINE = 62
    FISH_TANK_PORT = 63
    FISH = 64
    SOLAR_COLLECTOR = 65
    FORGE = 66
    GIVING_TREE = 67
    GIVING_TREE_STUMP = 68
    STEAM_BLOCK = 69  # lol hehe 69 lol
    STEAM_PAIN_BLOCK = 70
    STEAM_MUSIC_BLOCK = 71
    SILKWORM = 72
    SEWING_MACHINE = 73
    COUNTRY_FLAG = 74
    LOBSTER_TRAP = 75
    PAINTING_EASEL = 76
    BATTLE_PET_CAGE = 77
    PET_TRAINER = 78
    STEAM_ENGINE = 79
    LOCK_BOT = 80
    SPECIAL_WEATHER_MACHINE = 81
    SPIRIT_STORAGE_UNIT = 82
    DISPLAY_SHELF = 83
    VIP_ENTRANCE = 84
    CHALLENGE_TIMER = 85
    CHALLENGE_FLAG = 86
    FISH_MOUNT = 87
    PORTRAIT = 88
    SPECIAL_WEATHER_MACHINE_2 = 89
    FOSSIL = 90
    FOSSIL_PREP_STATION = 91
    DNA_PROCESSOR = 92
    HOWLER = 93
    VALHOWLA_TREASURE = 94
    CHEMSYNTH_PROCESSOR = 95
    CHEMSYNTH_TANK = 96
    STORAGE_BOX = 97
    COOKING_OVEN = 98
    AUDIO_BLOCK = 99
    GEIGER_CHARGER = 100
    ADVENTURE_BEGIN = 101
    TOMB_ROBBER = 102
    BALLOON_O_MATIC = 103
    TEAM_ENTRACE_PUNCH = 104
    TEAM_ENTRANCE_GROW = 105
    TEAM_ENTRACE_BUILDER = 106
    ARTIFACT = 107
    JELLY_BLOCK = 108
    TRAINING_PORT = 109
    FISHING_BLOCK = 110
    MAGPLANT = 111
    MAGPLANT_REMOTE = 112
    CYBLOCK_BOT = 113
    CYBLOCK_COMMAND = 114
    LUCKY_TOKEN = 115
    GROWSCAN = 116
    CONTAINMENT_FIELD_POWER_NODE = 117
    SPIRIT_BOARD = 118
    WORLD_ARCHITECT = 119
    STARTOPIA_BLOCK = 120
    # UNKNOWN3 = 121
    TOGGLEABLE_MULTI_FRAMED_ANIMATED_BLOCK = 122
    AUTOBREAK_BLOCKS = 123
    AUTOBREAK_TREES = 124
    AUTOBREAK = 125
    STORM_CLOUD = 126
    VANISH_ON_IMPACT = 127
    PUDDLE_BLOCK = 128
    ROOT_CUTTING = 129
    SAFE_VAULT = 130
    ANGELIC_COUNTING_CLOUD = 131
    MINING_EXPLOSIVES = 132
    # UNKNOWN4 = 133
    INFINITY_WEATHER_MACHINE = 134
    SLIMING_BLOCK = 135
    ACID_PAIN_BLOCK = 136
    # UNKNOWN5 = 137
    WAVING_INFLATABLE_ARM_GUY = 138
    # UNKNOWN6 = 139
    PINEAPPLE_GUZZLER = 140  # guzzle deez nuts
    KRANKENS_GALACTIC_BLOCK = 141
    FRIENDS_ENTRANCE = 142


class ItemVisualEffectType(IntEnumBase):
    NONE = 0


class ItemCollisionType(IntEnumBase):
    NONE = 0  # no collision
    SOLID = 1  # proper solid
    PLATFORM = 2  # can pass through, just not go down
    ENTRANCE = 3  # entrance, can pass through with access
    TOGGLEABLE_SOLID = 4  # dragon gate, laboratory, etc
    ONE_WAY = 5  # one-way block, one side collision
    VIP_ENTRANCE = 6  # vip entrance, can pass through with access
    VERTICAL_DOWN = 7  # vertical down, can't go up
    ADVENTURE = 8  # adventure, can pass through with adventure item collected
    TOGGLEABLE_DEADLY = 9  # evil eye, steam spikes, etc (deadly if on)
    TEAM_ENTRANCE = 10  # team entrance, can pass through if on team (p, g, b)
    GUILD_ENTRANCE = 11  # guild entrance, can pass through if in guild
    TIMED_COLLISION = 12  # timed collision, collision on for x time
    FRIENDS_ENTRANCE = 13  # friends entrance, can pass through if on friends list (ig idk)


class ItemProperty(IntFlag):
    FLIPPABLE = 1 << 0
    EDITABLE = 1 << 1
    SEEDLESS = 1 << 2
    PERMANENT = 1 << 3
    DROPLESS = 1 << 4
    NO_SELF = 1 << 5
    NO_SHADOW = 1 << 6
    LOCK = 1 << 7
    BETA = 1 << 8
    AUTO_PICKUP = 1 << 9
    MOD = 1 << 10
    RAND_GROW = 1 << 11
    PUBLIC = 1 << 12
    FOREGROUND = 1 << 13
    HOLIDAY = 1 << 14
    UNTRADEABLE = 1 << 15


class ItemStorageType(IntEnumBase):
    SINGLE_FRAME = 1


class ItemMaterialType(IntEnumBase): ...
