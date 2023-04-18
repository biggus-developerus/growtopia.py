__all__ = ("PlayerTribute",)

from typing import BinaryIO, Optional, Union

from .utils import hash_


class PlayerTribute:
    def __init__(self, data: Union[str, bytes, BinaryIO]) -> None:
        self.content: bytes
        self.hash: int = 0

        if isinstance(data, str):
            with open(data, "rb") as f:
                self.content = f.read()
        elif isinstance(data, bytes):
            self.content = data
        elif isinstance(data, BinaryIO):
            self.content = data.read()
        else:
            raise ValueError("Invalid data type passed into initialiser.")

    def parse(self) -> None:
        self.hash = hash_(self.content)
