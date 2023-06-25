__all__ = ("PlayerLoginInfo",)

from dataclasses import dataclass


@dataclass
class PlayerLoginInfo:
    """
    A dataclass that contains all the keys and values that are sent to the server when a client's logging in.
    """

    requested_name: str = ""
    tank_id_name: str = ""
    tank_id_pass: str = ""
    f: str = ""
    protocol: str = ""
    game_version: str = ""
    fz: str = ""
    lmode: str = ""
    cbits: str = ""
    player_age: str = ""
    gdpr: str = ""
    category: str = ""
    total_playtime: str = ""
    klv: str = ""
    hash2: str = ""
    meta: str = ""
    fhash: str = ""
    rid: str = ""
    platform_id: str = ""
    device_version: str = ""
    country: str = ""
    hash: str = ""
    mac: str = ""
    wk: str = ""
    zf: str = ""
