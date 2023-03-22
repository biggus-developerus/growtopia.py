__all__ = ("Variant",)

import struct
from typing import Any

from .enums import VariantType

serialisers = {
    VariantType.INT: lambda data: bytearray(data.to_bytes(4, "little")),
    VariantType.UINT: lambda data: bytearray(data.to_bytes(4, "little", signed=True)),
    VariantType.FLOAT: lambda data: bytearray(struct.pack("f", data)),
    VariantType.STR: lambda data: bytearray(
        len(data).to_bytes(4, "little") + data.encode()
    ),
}


class Variant:
    def __init__(self, value: Any, type_: VariantType = None) -> None:
        self.type: VariantType = (
            type_ if type_ else VariantType[type(value).__name__.upper()]
        )
        self.value: Any = value
        self.data: bytearray = bytearray()

    def serialise(self, index: int) -> bytearray:
        self.data = bytearray(
            index.to_bytes(1, "little")
            + self.type.value.to_bytes(1, "little")
            + serialisers[self.type](self.value)
        )

        return self.data