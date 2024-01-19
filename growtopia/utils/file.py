__all__ = ("File",)

from typing import Union

from .buffer import (
    ReadBuffer,
    WriteBuffer
)
from .proton import (
    decrypt,
    proton_hash
)


class File:
    def __init__(self) -> None:
        self.buffer: Union[ReadBuffer, WriteBuffer]  # ABC

    @staticmethod
    def is_items_data(path_or_data: Union[str, memoryview]) -> bool:
        if not isinstance(path_or_data, str) and not isinstance(path_or_data, memoryview):
            raise TypeError(f"Expected str or memoryview, got {type(path_or_data)}")

        buff = ReadBuffer.load(path_or_data)
        buff.skip(
            2 + 4 + 8
        )  # version, item count, id, editable_type, category, action_type, hit_sound_type

        return decrypt(buff.read_string(), 0) == "Blank"

    @staticmethod
    def is_player_tribute(path_or_data: Union[str, memoryview]) -> bool:
        if not isinstance(path_or_data, str) and not isinstance(path_or_data, memoryview):
            raise TypeError(f"Expected str or memoryview, got {type(path_or_data)}")

        raise NotImplementedError("TODO: implement this")

    def _get_hash(self) -> int:
        return getattr(self, "hash", None) or proton_hash(self.buffer.data)

    def save(self, path: str) -> None:
        with open(path, "wb") as f:
            f.write(bytes(self.buffer.data))
