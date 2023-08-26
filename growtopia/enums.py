__all__ = (
    "EventID",
    "Colour",
)

from enum import StrEnum
from typing import Any


class EventID(StrEnum):
    """
    An enumeration of all dispatchable events.
    """

    # General events (not related to ENet / Growtopia)
    ON_UNKNOWN = "on_unknown"
    ON_UNHANDLED = "on_unhandled"
    ON_CLEANUP = "on_cleanup"
    ON_READY = "on_ready"

    # ENet events
    ON_CONNECT = "on_connect"
    ON_DISCONNECT = "on_disconnect"
    ON_RECEIVE = "on_receive"

    # Packet events
    ON_HELLO = "on_hello"
    ON_MALFORMED_PACKET = "on_malformed_packet"
    ON_LOGIN_REQUEST = "on_login_request"
    ON_ACTION_QUIT = "on_quit"
    ON_DIALOG_RETURN = "on_dialog_return"
    ON_PLAY_SFX = "on_play_sfx"
    ON_LOG = "on_log"
    ON_LOGON_FAIL = "on_logon_fail"
    ON_REFRESH_ITEM_DATA = "on_refresh_item_data"
    ON_REFRESH_PLAYER_TRIBUTE_DATA = "on_refresh_player_tribute_data"
    ON_ENTER_GAME = "on_enter_game"
    ON_JOIN_REQUEST = "on_join_request"
    ON_QUIT_TO_EXIT = "on_quit_to_exit"
    ON_INPUT = "on_input"
    ON_WRENCH = "on_wrench"
    ON_GROWID = "on_growid"
    ON_STORE = "on_store"
    ON_FRIENDS = "on_friends"
    ON_EVENTMENU = "on_eventmenu"

    # Call function events
    OnSuperMain = "on_super_main"
    OnSendToServer = "on_send_to_server"
    OnConsoleMessage = "on_console_message"
    OnTradeStatus = "on_trade_status"
    OnDialogRequest = "on_dialog_request"
    OnRequestWorldSelectMenu = "on_request_world_select_menu"
    OnForceTradeEnd = "on_force_trade_end"

    # Update events
    ON_STATE_UPDATE = "on_state_update"
    ON_CALL_FUNCTION = "on_call_function"
    ON_UPDATE_STATUS = "on_update_status"

    ON_TILE_CHANGE_REQUEST = "on_tile_change_request"
    ON_TILE_PUNCH = "on_tile_punch"
    ON_TILE_PLACE = "on_tile_place"

    ON_SEND_MAP_DATA = "on_send_map_data"
    ON_SEND_TILE_UPDATE_DATA = "on_send_tile_update_data"
    ON_SEND_TILE_UPDATE_DATA_MULTIPLE = "on_send_tile_update_data_multiple"
    ON_TILE_ACTIVATE_REQUEST = "on_tile_activate_request"
    ON_TILE_APPLY_DAMAGE = "on_tile_apply_damage"
    ON_SEND_INVENTORY_STATE = "on_send_inventory_state"
    ON_ITEM_ACTIVATE_REQUEST = "on_item_activate_request"
    ON_ITEM_ACTIVATE_OBJECT_REQUEST = "on_item_activate_object_request"
    ON_SEND_TILE_TREE_STATE = "on_send_tile_tree_state"
    ON_MODIFY_ITEM_INVENTORY = "on_modify_item_inventory"
    ON_ITEM_CHANGE_OBJECT = "on_item_change_object"
    ON_SEND_LOCK = "on_send_lock"
    ON_SEND_ITEMS_DATA = "on_send_items_data"
    ON_SEND_PARTICLE_EFFECT = "on_send_particle_effect"
    ON_SET_ICON_STATE = "on_set_icon_state"
    ON_ITEM_EFFECT = "on_item_effect"
    ON_SET_CHARACTER_STATE = "on_set_character_state"
    ON_PING_REPLY = "on_ping_reply"
    ON_PING_REQUEST = "on_ping_request"
    ON_GOT_PUNCHED = "on_got_punched"
    ON_APP_CHECK_RESPONSE = "on_app_check_response"
    ON_APP_INTEGRITY_FAIL = "on_app_integrity_fail"
    ON_UPDATE_DISCONNECT = "on_update_disconnect"
    ON_BATTLE_JOIN = "on_battle_join"
    ON_BATTLE_EVENT = "on_battle_event"
    ON_USE_DOOR = "on_use_door"
    ON_SEND_PARENTAL = "on_send_parental"
    ON_GONE_FISHIN = "on_gone_fishin"
    ON_STEAM = "on_steam"
    ON_PET_BATTLE = "on_pet_battle"
    ON_NPC = "on_npc"
    ON_SPECIAL = "on_special"
    ON_SEND_PARTICLE_EFFECT_V2 = "on_send_particle_effect_v2"
    ON_ACTIVE_ARROW_TO_ITEM = "on_active_arrow_to_item"
    ON_SELECT_TILE_INDEX = "on_select_tile_index"
    ON_SEND_PLAYER_TRIBUTE_DATA = "on_send_player_tribute_data"

    @classmethod
    def _missing_(cls, _: object) -> Any:
        return cls("on_unknown")


class Colour(StrEnum):
    """
    An enumeration of all text colours that can be used.
    """

    DEFAULT = "`o"
    LIGHT_CYAN = "`1"
    GREEN = "`2"
    LIGHT_BLUE = "`3"
    RED = "`4"
    LIGHT_PURPLE = "`5"
    BEIGE = "`6"
    LIGHT_GRAY = "`7"
    ORANGE = "`8"
    LIGHT_YELLOW = "`9"
    VERY_LIGHT_CYAN = "`!"
    LIGHT_PINK = "`@"
    PURPLE = "`#"
    VERY_LIGHT_YELLOW = "`$"
    VERY_LIGHT_GREEN = "`^"
    VERY_LIGHT_PINK = "`&"
    WHITE = "`w"  # w and 0 are the same
    LIGHT_BEIGE = "`o"
    BLACK = "`b"
    PINK = "`p"
    DARK_BLUE = "`q"
    BLUE = "`e"
    LIGHT_GREEN = "`r"
    DARK_GREEN = "`t"
    DARK_GRAY = "`a"
    GRAY = "`s"
    CYAN = "`c"
