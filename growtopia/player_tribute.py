__all__ = ("PlayerTribute",)


class PlayerTribute:
    def __init__(self, path: str) -> None:
        with open(path, "rb") as f:
            self.content: bytes = f.read()

        self.hash: int = 0
