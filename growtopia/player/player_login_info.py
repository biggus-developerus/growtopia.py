__all__ = ("PlayerLoginInfo",)

from dataclasses import dataclass

from ..protocol import TextPacket


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
    reconnect: str = ""

    # SUB SERVER KEYS
    user: str = ""
    token: str = ""
    doorID: str = ""
    UUIDToken: str = ""

    @property
    def packet(self) -> TextPacket:
        """
        Returns
        -------
        TextPacket
            The packet that contains all the keys and values.
        """
        packet = TextPacket()
        packet.kvps = self.__dict__.copy()

        return packet
