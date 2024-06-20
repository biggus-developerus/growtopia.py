__all__ = ("Packer",)

from typing import (
    Callable,
    Self,
    Type,
    get_origin,
)

from growtopia._types import (
    OptionalPack,
    Pack,
)

from .packers import *


class Packer:
    _pack_mapping: dict[Type, Callable[..., bytearray]]
    _min_size: int
    _optional_members: list[str]

    @classmethod
    def from_bytes(cls, data: bytearray, *default_args, **default_kwargs) -> "Self":
        obj = cls(*default_args, **default_kwargs)
        obj.unpack(data)

        return obj

    def __new__(cls, *_, **__) -> "Self":
        if getattr(cls, "_pack_mapping", None):
            return super().__new__(cls)

        # we're guessing that whoever (me) will use this would actually have those (obj) attrs initialised in the child class (we r not doing that for them lol.)
        cls._pack_mapping = {}
        cls._min_size = 0
        cls._optional_members = []

        count = len(cls.__annotations__.items())

        for i, item in enumerate(cls.__annotations__.items()):
            attr, attr_type = item
            type_origin = get_origin(attr_type)
            origin_of_next_attr = get_origin(
                list(cls.__annotations__.items())[i + 1 if i + 1 < count else i][1]
            )

            if attr_type not in TYPE_TO_PACK_MAPPING and not type_origin in [Pack, OptionalPack]:
                continue

            if attr_type not in TYPE_TO_PACK_MAPPING and type_origin in [Pack, OptionalPack]:
                raise ValueError(
                    f"Unhandled type of `Pack`/`OptionalPack` type origin. Available (packable) types are {', '.join([str(key) for key in TYPE_TO_PACK_MAPPING.keys()])}"
                )

            if type_origin is OptionalPack and origin_of_next_attr is Pack:
                raise ValueError("Non-optional members cannot follow optional members.")

            cls._pack_mapping[attr] = TYPE_TO_PACK_MAPPING[attr_type]
            cls._min_size += (
                TYPE_TO_SIZE_MAPPING[attr_type] if not type_origin is OptionalPack else 0
            )

            if type_origin is OptionalPack:
                cls._optional_members.append(attr)

        return super().__new__(cls)

    def pack(self) -> bytearray:
        data = bytearray()

        for attr, packer in self._pack_mapping.items():
            val = getattr(self, attr)

            if val is None and attr not in self._optional_members:
                raise ValueError(
                    f"{attr} cannot be None as it's not an optional member (obv lel fix yer kode baddei.)"
                )

            if val is not None:
                data += packer[0](val)

        return data

    def unpack(self, data: bytearray) -> bool:
        offset = 0
        data_len = len(data)

        if data_len < self._min_size:
            return False

        for attr, packer in self._pack_mapping.items():
            if offset >= data_len and attr in self._optional_members:
                break

            size, val = packer[1](data[offset:])

            if size == -1:
                return False

            offset += size

            setattr(self, attr, val)

        return True
