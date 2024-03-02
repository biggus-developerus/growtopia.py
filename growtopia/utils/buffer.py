__all__ = ("Buffer",)

from typing import (
    Literal,
    Optional,
    Union,
)

from typeguard import (
    typechecked,
)

from ..utils.compression import (
    CompressionType,
    zlib_compress,
    zlib_decompress,
)


class Buffer:
    @typechecked
    def __init__(self, data: Optional[bytearray] = None) -> None:
        self.__data: bytearray = data or bytearray()
        self.__offset: int = 0

    @staticmethod
    def load(path_or_data: Union[str, bytearray]) -> "Buffer":
        if isinstance(path_or_data, str):
            with open(path_or_data, "rb") as f:
                return Buffer(bytearray(f.read()))

        return Buffer(path_or_data)

    def save_to_file(self, path: str) -> None:
        with open(path, "wb") as f:
            f.write(self.data)

    def compress(self, compression_type: CompressionType) -> None:
        if compression_type == CompressionType.ZLIB:
            self.__data = bytearray(zlib_compress(self.data))
        else:
            raise ValueError(f"Unknown compression type: {compression_type}")

    def decompress(self, compression_type: CompressionType) -> None:
        if compression_type == CompressionType.ZLIB:
            self.__data = bytearray(zlib_decompress(self.data))
        else:
            raise ValueError(f"Unknown compression type: {compression_type}")

    def skip(self, size: int) -> None:
        self.__offset += size

    def reset_offset(self) -> None:
        self.__offset = 0

    def read(self, size: int) -> bytearray:
        val = self.data[self.offset : self.offset + size]
        self.skip(size)

        return val

    def read_int(self, int_size: int = 4, byteorder: Literal["little", "big"] = "little") -> int:
        return int.from_bytes(self.read(int_size), byteorder=byteorder)

    def read_str(self, str_size: int, encoding: str = "utf-8") -> str:
        return self.read(str_size).decode(encoding)

    def write(self, data: Union[bytes, bytearray]) -> None:
        self.__data.extend(data)
        self.skip(len(data))

    def write_int(
        self, value: int, int_size: int = 4, byteorder: Literal["little", "big"] = "little"
    ) -> None:
        self.write(value.to_bytes(int_size, byteorder=byteorder))

    def write_str(self, value: str, encoding: str = "utf-8") -> None:
        self.write(value.encode(encoding))

    @property
    def offset(self) -> int:
        return self.__offset

    @property
    def data(self) -> bytearray:
        return self.__data

    @property
    def data_at_offset(self) -> bytearray:
        return self.__data[self.__offset :]
