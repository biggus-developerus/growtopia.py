__all__ = ("PlayerLoginInfo",)


class PlayerLoginInfo:
    def __init__(self) -> None:
        self.requested_name: str = ""
        self.tank_id_name: str = ""
        self.tank_id_pass: str = ""
