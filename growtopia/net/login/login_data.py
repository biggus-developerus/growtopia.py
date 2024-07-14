__all__ = ("LoginData",)

from dataclasses import (
    dataclass,
)
from urllib import parse


@dataclass
class LoginData:
    requestedName: str = ""
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

    # TODO: handle klv & hash generation internally for the user
    # TODO: helper methods (i.e LoginData.new_ios(), LoginData.new_android(), etc.)

    def url_encode(self) -> str:
        return "\n".join([parse.quote(f"{key}|{value}") for key, value in self.__dict__.items()])
