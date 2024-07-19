__all__ = ("AllStr", "LengthPrefixedData")

from packer import (
    TypeDescriptor,
)


class AllStr(TypeDescriptor):
    __data_size__ = 0  # should always be optional cuz laikeee ya??

    @classmethod
    def pack(cls, value: str) -> bytes:
        return value.encode()

    @classmethod
    def unpack(cls, data: bytearray) -> tuple[int, str]:
        return len(data), data.decode("utf-8")


class LengthPrefixedData(TypeDescriptor):
    __data_size__ = 4  # size of the prefix (length prefix)

    @classmethod
    def pack(cls, val: bytes) -> bytes:
        return int.to_bytes(len(val), cls.__data_size__, "little") + val

    @classmethod
    def unpack(cls, data: bytearray) -> tuple[int, bytes]:
        data_len = int.from_bytes(data[: cls.__data_size__], "little")
        return data_len + cls.__data_size__, data[cls.__data_size__ : cls.__data_size__ + data_len]
