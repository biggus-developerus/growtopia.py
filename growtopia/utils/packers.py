__all__ = (
    "_pack_lps",
    "_unpack_lps",
    "TYPE_TO_PACK_MAPPING",
    "TYPE_TO_SIZE_MAPPING",
)

from typing import (
    Callable,
    Optional,
    Tuple,
)

from .._types import (
    LengthPrefixedStr,
    Pack,
    int8,
    int16,
    int32,
)


def _pack_lps(val: LengthPrefixedStr) -> bytearray:
    return bytearray(len(val).to_bytes(2, "little") + val.encode())


def _unpack_lps(data: bytearray) -> Tuple[int, Optional[LengthPrefixedStr]]:
    if len(data) < 2:
        return -1, None

    str_len = int.from_bytes(data[:2], "little")

    if str_len < 0:
        return -1, None
    if str_len == 0:
        return 2, ""

    return 2 + str_len, data[2 : 2 + str_len].decode()


def _make_int_packer(size: int) -> Callable[[int], bytearray]:
    return lambda val: bytearray(val.to_bytes(size, "little"))


def _make_int_unpacker(size: int) -> Callable[[bytearray], Tuple[int, Optional[int]]]:
    return lambda data: (
        (-1, None) if len(data) < size else (size, int.from_bytes(data[:size], "little"))
    )


TYPE_TO_PACK_MAPPING = {
    Pack[int32]: (_make_int_packer(4), _make_int_unpacker(4)),
    Pack[int16]: (_make_int_packer(2), _make_int_unpacker(2)),
    Pack[int8]: (_make_int_packer(1), _make_int_unpacker(1)),
    Pack[LengthPrefixedStr]: (_pack_lps, _unpack_lps),
}

TYPE_TO_SIZE_MAPPING = {  # used to determine min required size of data (when unpacking)
    Pack[int32]: 4,
    Pack[int16]: 2,
    Pack[int8]: 1,
    Pack[LengthPrefixedStr]: 2,
}
