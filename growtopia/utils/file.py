__all__ = ("File",)

from abc import ABC
from typing import (
    Optional,
    Union,
)

from .buffer import (
    ReadBuffer,
    WriteBuffer,
)
from .proton import (
    decrypt,
    proton_hash,
)


class File(ABC):
    def __init__(self, path: str = "") -> None:
        self.buffer: Union[ReadBuffer, WriteBuffer]
        self.hash: int

        self.path: str = path

    @staticmethod
    def is_items_data(path_or_data: Union[str, memoryview]) -> bool:
        if not isinstance(path_or_data, str) and not isinstance(path_or_data, memoryview):
            raise TypeError(f"Expected str or memoryview, got {type(path_or_data)}")

        buff = ReadBuffer.load(path_or_data)
        buff.skip(
            2 + 4 + 8
        )  # version, item count, id, editable_type, category, action_type, hit_sound_type

        # would work only IF the user wasn't using a FULLY custom items.dat
        # e.g they fucking replaced blank with some other shit or messed up the order
        # if they are then.. they should go ahead n meddle with this cancer sob x69420

        return decrypt(buff.read_string(), 0) == "Blank"

    @staticmethod
    def is_player_tribute(path_or_data: Union[str, memoryview]) -> bool:
        if not isinstance(path_or_data, str) and not isinstance(path_or_data, memoryview):
            raise TypeError(f"Expected str or memoryview, got {type(path_or_data)}")

        raise NotImplementedError("TODO: implement this")

    def _get_hash(self) -> int:
        if self.hash:
            return self.hash

        self.hash = proton_hash(self.buffer.data)

        return self.hash

    def save(self, path: Optional[str] = None) -> None:
        with open(path or self.path, "wb") as f:
            f.write(bytes(self.buffer.data))
