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

    @property
    def packet(self) -> TextPacket:
        """
        Returns
        -------
        TextPacket
            The packet that contains all the keys and values.
        """
        packet = TextPacket()
        packet.text = f"requestedName|{self.requestedName}\ntankIDName|{self.tankIDName}\ntankIDPass|{self.tankIDPass}\nf|{self.f}\nprotocol|{self.protocol}\ngame_version|{self.game_version}\nfz|{self.fz}\nlmode|{self.lmode}\ncbits|{self.cbits}\nplayer_age|{self.player_age}\nGDPR|{self.GDPR}\ncategory|{self.category}\ntotalPlaytime|{self.totalPlaytime}\nklv|{self.klv}\nhash2|{self.hash2}\nmeta|{self.meta}\nfhash|{self.fhash}\nrid|{self.rid}\nplatformID|{self.platformID}\ndeviceVersion|{self.deviceVersion}\ncountry|{self.country}\nhash|{self.hash}\nmac|{self.mac}\nwk|{self.wk}\nzf|{self.zf}\n"

        return packet
