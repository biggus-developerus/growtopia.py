__all__ = ("zlib_compress", "zlib_decompress", "CompressionType")

from enum import Enum
from typing import Union
from zlib import (
    Z_BEST_COMPRESSION,
    compress,
    decompress,
)


class CompressionType(Enum):
    ZLIB = 0


def zlib_compress(data: Union[memoryview, bytearray], level: int = Z_BEST_COMPRESSION) -> bytearray:
    return bytearray(compress(data, level=level))


def zlib_decompress(data: Union[memoryview, bytearray]) -> bytearray:
    return bytearray(decompress(data))
