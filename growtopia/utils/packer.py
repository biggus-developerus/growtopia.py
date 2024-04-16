__all__ = ("Packer",)

from typing import (
    Callable,
    Type,
)

from .packers import *


class Sentinel:
    pass


SENTINEL = Sentinel()


class Packer:
    _pack_mapping: dict[Type, Callable[..., bytearray]]
    _min_size: int

    @classmethod
    def from_bytes(cls, data: bytearray) -> "Packer":
        return cls().unpack(data)

    def __new__(cls, *_, **__) -> "Packer":
        if getattr(cls, "_pack_mapping", None):
            return super().__new__(cls)

        # we're guessing that whoever (me) will use this would actually have those (obj) attrs initialised in the child class (we r not doing that for them lol.)
        cls._pack_mapping = {}
        cls._min_size = 0
        for attr, attr_type in cls.__annotations__.items():
            if attr_type not in TYPE_TO_PACK_MAPPING:
                continue

            cls._pack_mapping[attr] = TYPE_TO_PACK_MAPPING[attr_type]
            cls._min_size += TYPE_TO_SIZE_MAPPING[attr_type]

        return super().__new__(cls)

    def pack(self) -> bytearray:
        data = bytearray()

        for attr, packer in self._pack_mapping.items():
            data += packer[0](getattr(self, attr))

        return data

    def unpack(self, data: bytearray) -> bool:
        offset = 0
        data_len = len(data)

        if data_len < self._min_size:
            return False

        for attr, packer in self._pack_mapping.items():
            if offset > data_len:
                return False

            size, val = packer[1](data[offset:])

            if size == -1:
                return False

            offset += size

            setattr(self, attr, val)

        return True
