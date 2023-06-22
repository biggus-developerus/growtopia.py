__all__ = ("PlayerLoginInfo",)


class PlayerLoginInfo:
    def __init__(self, kvps: dict[str, str] = {}) -> None:
        self.requested_name: str = ""
        self.tank_id_name: str = ""
        self.tank_id_pass: str = ""
        self.f: str = ""
        self.protocol: str = ""
        self.game_version: str = ""
        self.fz: str = ""
        self.lmode: str = ""
        self.cbits: str = ""
        self.player_age: str = ""
        self.gdpr: str = ""
        self.category: str = ""
        self.total_playtime: str = ""
        self.klv: str = ""
        self.hash2: str = ""
        self.meta: str = ""
        self.fhash: str = ""
        self.rid: str = ""
        self.platform_id: str = ""
        self.device_version: str = ""
        self.country: str = ""
        self.hash: str = ""
        self.mac: str = ""
        self.wk: str = ""
        self.zf: str = ""

        self.set_attrs(kvps)

    def set_attrs(self, kvps: dict[str, str]) -> None:
        for key, value in kvps.items():
            setattr(self, key, value)
