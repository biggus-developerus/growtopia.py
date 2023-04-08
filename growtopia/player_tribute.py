__all__ = ("PlayerTribute",)

from .utils import hash_


class PlayerTribute:
    def __init__(self, path: str) -> None:
        with open(path, "rb") as f:
            self.content: bytes = f.read()

        self.hash: int = 0

    def parse(self) -> None:
        self.hash = hash_(self.content)
