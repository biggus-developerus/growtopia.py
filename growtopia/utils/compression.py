__all__ = ("zlib_compress", "zlib_decompress", "CompressionType")


from enum import Enum
from zlib import (
    Z_BEST_COMPRESSION,
    compress,
    decompress,
)

from typeguard import (
    typechecked,
)


class CompressionType(Enum):
    ZLIB = 0


@typechecked
def zlib_compress(data: bytearray) -> bytes:
    return compress(data, level=Z_BEST_COMPRESSION)


@typechecked
def zlib_decompress(data: bytearray) -> bytes:
    return decompress(data)
