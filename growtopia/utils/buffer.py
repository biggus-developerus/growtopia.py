__all__ = (
    "ReadBuffer",
    "WriteBuffer",
)

from typing import Union

from ..decorators import (
    type_checker,
)


class BuffBase:
    def __len__(self) -> int:
        raise NotImplementedError

    def __bool__(self) -> bool:
        raise NotImplementedError

    def __getitem__(self, _: int) -> int:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<Buffer size={len(self)}>"

    def __str__(self) -> str:
        return repr(self)


class ReadBuffer(BuffBase):
    @type_checker
    def __init__(self, data: memoryview) -> None:
        self.data: memoryview = data.toreadonly() if not data.readonly else data
        self.offset: int = 0

    def skip(self, size: int) -> None:
        self.offset += size

    def get_chunk(self, start: int, end: int) -> "ReadBuffer":
        return ReadBuffer(self.data[start:end])

    def get_bytes(self, start: int, end: int) -> bytes:
        return self.get_chunk(start, end).data.tobytes()

    def read_bytes(self, size: int) -> bytes:
        value = self.get_bytes(self.offset, self.offset + size)
        self.offset += size

        return value

    def read_int(self, int_size: int = 4) -> int:
        value = int.from_bytes(self.get_bytes(self.offset, self.offset + int_size), "little")
        self.offset += int_size

        return value

    def read_string(self, length_int_size: int = 4, *, string_size: int = 0, is_items_data_string: bool = False) -> str:
        if string_size == 0:
            length = self.read_int(length_int_size)
        else:
            length = string_size

        if is_items_data_string:
            value = "".join(chr(i) for i in self.get_bytes(self.offset, self.offset + length))
        else:
            value = self.get_bytes(self.offset, self.offset + length).decode()

        self.offset += length
        return value

    def __len__(self) -> int:
        return len(self.data)

    def __bool__(self) -> bool:
        return bool(self.data)

    def __getitem__(self, index: int) -> int:
        return self.data[index]

    @staticmethod
    @type_checker
    def load_file(path: str) -> "ReadBuffer":
        with open(path, "rb") as file:
            return ReadBuffer(memoryview(file.read()))

    @staticmethod
    @type_checker
    def load_bytes(data: Union[bytes, bytearray]) -> "ReadBuffer":
        return ReadBuffer(memoryview(data))

    @staticmethod  # PBM = Path, Bytes, Memoryview
    @type_checker
    def load(pbm: Union[str, bytes, memoryview]) -> "ReadBuffer":
        if isinstance(pbm, str):
            return ReadBuffer.load_file(pbm)
        elif isinstance(pbm, (bytes, bytearray)):
            return ReadBuffer.load_bytes(pbm)
        elif isinstance(pbm, memoryview):
            return ReadBuffer(pbm)


class WriteBuffer(BuffBase):
    def __init__(self) -> None:
        self.__data: bytearray = bytearray()

    def write_bytes(self, data: bytes) -> None:
        self.__data += data

    def write_int(self, value: int, int_size: int = 4) -> None:
        self.write_bytes(value.to_bytes(int_size, "little"))

    def write_string(self, value: str, length_int_size: int = 4) -> None:
        encoded_value = value.encode()
        if length_int_size > 0:
            self.write_int(len(encoded_value), length_int_size)
        self.write_bytes(encoded_value)

    @property
    def data(self) -> memoryview:
        return memoryview(self.__data).toreadonly()

    def __len__(self) -> int:
        return len(self.__data)

    def __bool__(self) -> bool:
        return bool(self.__data)

    def __getitem__(self, index: int) -> int:
        return self.__data[index]

    def __setitem__(self, index: int, value: int) -> None:
        self.__data[index] = value
