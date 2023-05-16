__all__ = ("Variant",)

import struct
from typing import Union

from .enums import VariantType


class Variant:
    _serialisers = {
        VariantType.INT: lambda data: bytearray(
            data.to_bytes(4, "little"), signed=True
        ),
        VariantType.UINT: lambda data: bytearray(data.to_bytes(4, "little")),
        VariantType.FLOAT: lambda data: bytearray(struct.pack("f", data)),
        VariantType.STR: lambda data: bytearray(
            len(data).to_bytes(4, "little") + data.encode()
        ),
        VariantType.NONE: lambda _: bytearray(),
    }

    _deserialisers = {
        VariantType.INT: lambda data: int.from_bytes(data[:4], "little", signed=True),
        VariantType.UINT: lambda data: int.from_bytes(data[:4], "little"),
        VariantType.FLOAT: lambda data: struct.unpack("f", data[:4])[0],
        VariantType.STR: lambda data: data[
            4 : int.from_bytes(data[:4], "little") + 4
        ].decode(),
        VariantType.NONE: lambda _: None,
    }

    def __init__(
        self, value: Union[str, int, float], type_: VariantType = None
    ) -> None:
        self.type: VariantType = type_ or VariantType[type(value).__name__.upper()]
        self.value: Union[str, int, float] = value
        self.data: bytearray = bytearray()

    def serialise(self, index: int) -> bytearray:
        self.data = bytearray(
            index.to_bytes(1, "little")
            + self.type.value.to_bytes(1, "little")
            + self._serialisers[self.type](self.value)
        )

        return self.data

    @classmethod
    def from_bytes(cls, data: bytearray) -> "Variant":
        return cls(
            type_=(type_ := VariantType(int.from_bytes(data[1:2], "little"))),
            value=cls._deserialisers[type_](data[2:]),
        )
