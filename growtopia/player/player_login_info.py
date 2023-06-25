__all__ = ("PlayerLoginInfo",)

from dataclasses import dataclass


@dataclass
class PlayerLoginInfo:
    """
    A dataclass that contains all the keys and values that are sent to the server when a client's logging in.
    """

    requestedName: str = ""
    tankIDName: str = ""
    tankIDPass: str = ""
    f: str = ""
    protocol: str = ""
    game_version: str = ""
    fz: str = ""
    lmode: str = ""
    cbits: str = ""
    player_age: str = ""
    GDPR: str = ""
    category: str = ""
    totalPlaytime: str = ""
    klv: str = ""
    hash2: str = ""
    meta: str = ""
    fhash: str = ""
    rid: str = ""
    platformID: str = ""
    deviceVersion: str = ""
    country: str = ""
    hash: str = ""
    mac: str = ""
    wk: str = ""
    zf: str = ""
