__all__ = ("PlayerTribute",)

from typing import BinaryIO, Union


class PlayerTribute:
    def __init__(self, data: Union[str, bytes, BinaryIO]) -> None:
        self.content: bytes
        self.__hash: int = 0

        if isinstance(data, str):
            with open(data, "rb") as f:
                self.content = f.read()
        elif isinstance(data, bytes):
            self.content = data
        elif isinstance(data, BinaryIO):
            self.content = data.read()
        else:
            raise ValueError("Invalid data type passed into initialiser.")

    @property
    def hash(self) -> int:
        if self.__hash != 0:
            return self.__hash

        result = 0x55555555

        for i in self.content:
            result = (result >> 27) + (result << 5) + i & 0xFFFFFFFF

        self.__hash = result
        return int(result)

    def parse(self) -> None:
        print(self.hash)
