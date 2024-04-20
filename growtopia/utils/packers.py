__all__ = (
    "_pack_lps",
    "_unpack_lps",
    "TYPE_TO_PACK_MAPPING",
    "TYPE_TO_SIZE_MAPPING",
)

import struct
from typing import (
    Callable,
    Optional,
    Tuple,
)

from growtopia._types import (
    AllData,
    AllStr,
    LengthPrefixedData,
    LengthPrefixedStr,
    OptionalPack,
    Pack,
    int8,
    int16,
    int32,
)

def _pack_lps(val: str) -> bytes:
    return len(val).to_bytes(2, "little") + val.encode()


def _unpack_lps(data: bytearray) -> Tuple[int, Optional[str]]:
    if len(data) < 2:
        return -1, None

    str_len = int.from_bytes(data[:2], "little", signed=True)

    if str_len < 0:
        return -1, None
    if str_len == 0:
        return 2, ""

    return 2 + str_len, data[2 : 2 + str_len].decode()


def _pack_lpd(val: bytearray) -> bytearray:
    return bytearray(len(val).to_bytes(2, "little") + val)


def _unpack_lpd(data: bytearray) -> Tuple[int, Optional[bytearray]]:
    if len(data) < 2:
        return -1, None

    data_len = int.from_bytes(data[:2], "little")

    if data_len < 0:
        return -1, None
    if data_len == 0:
        return 2, ""

    return 2 + data_len, data[2 : 2 + data_len]


def _make_int_packer(size: int) -> Callable[[int], bytes]:
    return lambda val: val.to_bytes(size, "little", signed=True)


def _make_int_unpacker(size: int) -> Callable[[bytearray], Tuple[int, Optional[int]]]:
    return lambda data: (
        (-1, None)
        if len(data) < size
        else (size, int.from_bytes(data[:size], "little", signed=True))
    )


TYPE_TO_PACK_MAPPING = {}
TYPE_TO_SIZE_MAPPING = {}  # used to determine min required size of data (when unpacking)

for pack_type in [Pack, OptionalPack]:  # crazy ikr
    TYPE_TO_PACK_MAPPING.update(
        {
            pack_type[int32]: (_make_int_packer(4), _make_int_unpacker(4)),
            pack_type[int16]: (_make_int_packer(2), _make_int_unpacker(2)),
            pack_type[int8]: (_make_int_packer(1), _make_int_unpacker(1)),
            pack_type[LengthPrefixedStr]: (_pack_lps, _unpack_lps),
            pack_type[LengthPrefixedData]: (_pack_lpd, _unpack_lpd),
            pack_type[AllStr]: (
                lambda val: bytearray(val.encode()),
                lambda data: (len(data), data.decode()),
            ),
            pack_type[AllData]: (
                lambda val: bytearray(val),
                lambda data: (len(data), bytearray(data)),
            ),
            pack_type[float]: (
                lambda val: bytearray(struct.pack("f", val)),
                lambda data: (
                    (-1, None) if len(data[:4]) < 4 else (4, struct.unpack("f", data[:4])[0])
                ),
            ),
        }
    )

    TYPE_TO_SIZE_MAPPING.update(
        {
            pack_type[int32]: 4,
            pack_type[int16]: 2,
            pack_type[int8]: 1,
            pack_type[LengthPrefixedStr]: 2,
            pack_type[LengthPrefixedData]: 2,
            pack_type[float]: 4,
        }
    )
