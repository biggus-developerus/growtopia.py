__all__ = ("Buffer",)

import struct
from typing import (
    Literal,
    Optional,
    Union,
)

from .compression import (
    CompressionType,
    zlib_compress,
    zlib_decompress,
)
from .crypto import hash_data


class Buffer:
    __slots__ = ("__data", "__offset")

    @staticmethod
    def load(path_or_data: Union[str, bytearray]) -> "Buffer":
        if isinstance(path_or_data, str):
            with open(path_or_data, "rb") as f:
                return Buffer(bytearray(f.read()))

        return Buffer(path_or_data)

    def __init__(self, data: Optional[bytearray] = None) -> None:
        self.__data: bytearray = data or bytearray()
        self.__offset: int = 0

    def save_to_file(self, path: str) -> None:
        with open(path, "wb") as f:
            f.write(self.data)

    def hash(self) -> int:
        return hash_data(self.data)

    def compress(self, compression_type: CompressionType) -> None:
        if compression_type == CompressionType.ZLIB:
            self.__data = zlib_compress(self.view)
        else:
            raise ValueError(f"Unknown compression type: {compression_type}")

    def decompress(self, compression_type: CompressionType) -> None:
        if compression_type == CompressionType.ZLIB:
            self.__data = zlib_decompress(self.view)
        else:
            raise ValueError(f"Unknown compression type: {compression_type}")

    def skip(self, size: int) -> None:
        self.__offset += size

    def reset_offset(self) -> None:
        self.__offset = 0

    def read(self, size: int) -> bytearray:
        val = self.__data[self.offset : self.offset + size]
        self.skip(size)

        return val

    def read_view(self, size: int) -> memoryview:
        val = self.view[self.offset : self.offset + size]
        self.skip(size)

        return val

    def read_int(self, int_size: int = 4, byteorder: Literal["little", "big"] = "little") -> int:
        return int.from_bytes(self.read_view(int_size), byteorder=byteorder)

    def read_float(
        self,
        float_size: int = 4,
        fmt: Union[str, bytes] = "f",
    ) -> float:
        return struct.unpack(fmt, self.read(float_size))[0]

    def read_str(self, str_size: int, encoding: str = "utf-8") -> str:
        return self.read(str_size).decode(encoding)

    def write(self, data: Union[bytes, bytearray]) -> None:
        self.__data.extend(data)
        self.skip(len(data))

    def write_int(
        self, value: int, int_size: int = 4, byteorder: Literal["little", "big"] = "little"
    ) -> None:
        self.write(value.to_bytes(int_size, byteorder=byteorder))

    def write_float(
        self,
        value: float,
        fmt: Union[str, bytes] = "f",
    ) -> None:
        self.write(struct.pack(fmt, value))

    def write_str(self, value: str, encoding: str = "utf-8") -> None:
        self.write(value.encode(encoding))

    @property
    def offset(self) -> int:
        return self.__offset

    @property
    def data(self) -> bytearray:
        return self.__data

    @property
    def view(self) -> memoryview:
        return memoryview(self.__data).toreadonly()

    @property
    def size(self) -> int:
        return len(self)

    @property
    def size_remaining(self) -> int:
        return len(self) - self.offset

    @property
    def data_at_offset(self) -> bytearray:
        return self.__data[self.__offset :]

    def __bool__(self) -> bool:
        return bool(self.data)

    def __len__(self) -> int:
        return len(self.data)
