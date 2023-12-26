__all__ = ("ignored_attributes", "CDN_HOST", "CDN_ROUTE", "BLOCKED_PACKAGES", "SETTINGS")

"""
As new items.dat versions are being supported, new attributes are being added to the Item class. 
Meaning that older versions of the items.dat file will not be parsed correctly.
However, you are able to exclude attributes from being parsed for a specifc items.dat version,
by adding them to the ignored_attributes dict.

Example:
    items.dat version 15 introduces 4 new bytes to the items.dat file.
    old ignored_attributes:
        {    
            11 : ["flags3", "bodypart", "flags4", "flags5"],
            12 : ["flags4", "flags5"],
            13 : ["flags5"],
            14 : []
        }
    new ignored_attributes:
        {    
            11 : ["flags3", "bodypart", "flags4", "flags5"],
            12 : ["flags4", "flags5"],
            13 : ["flags5"],
            14 : ["flags6"],
            15 : []
        }
"""

ignored_attributes = {
    11: ["flags3", "bodypart", "flags4", "flags5", "unknown", "sit_file"],
    12: ["flags4", "flags5", "unknown", "sit_file"],
    13: ["flags5", "unknown", "sit_file"],
    14: ["unknown", "sit_file"],
    15: ["renderer"],
    16: [],
}

latest_game_version: float = 4.33  # used for world packet serialisation

# Default ONSUPERMAIN function arguments

CDN_HOST: str = "ubistatic-a.akamaihd.net"
CDN_ROUTE: str = "0098/654352/cache/"
BLOCKED_PACKAGES: str = "cc.cz.madkite.freedom org.aqua.gg idv.aqua.bulldog com.cih.gamecih2 com.cih.gamecih com.cih.game_cih cn.maocai.gamekiller com.gmd.speedtime org.dax.attack com.x0.strai.frep com.x0.strai.free org.cheatengine.cegui org.sbtools.gamehack com.skgames.traffikrider org.sbtoods.gamehaca com.skype.ralder org.cheatengine.cegui.xx.multi1458919170111 com.prohiro.macro me.autotouch.autotouch com.cygery.repetitouch.free com.cygery.repetitouch.pro com.proziro.zacro com.slash.gamebuster"
SETTINGS: str = "proto=189|choosemusic=audio/mp3/about_theme.mp3|active_holiday=0|wing_week_day=0|server_tick=8184975|clash_active=1|drop_lavacheck_faster=1|isPayingUser=1|usingStoreNavigation=1|enableInventoryTab=1|bigBackpack=1|"
