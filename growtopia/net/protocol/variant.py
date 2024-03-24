__all__ = ("Variant",)


from typing import (
    Optional,
    Union,
)

from utils import Buffer

from .enums import VariantType
from .variant_type import *


class Variant:
    def __init__(
        self,
        value: Union[str, int, float, tuple[int, int], tuple[int, int, int]],
        variant_type: Optional[VariantType] = None,
    ) -> None:
        if isinstance(value, tuple):
            vector_type = VariantType.VECTOR2 if len(value) == 2 else VariantType.VECTOR3

        self.variant_type: VariantType = vector_type or variant_type[type(value).__name__.upper()]
        self.value: Union[str, int, float] = value
        self.data: Buffer = Buffer()

    def serialize(self, index: int) -> Buffer:
        data: Buffer = Buffer()

        data.write_int(index, 1)
        data.write_int(self.variant_type, 1)

        value = VariantNone.serialise(self.value)

        if self.variant_type == VariantType.INT:
            value = VariantInt.serialise(self.value)
        elif self.variant_type == VariantType.UINT:
            value = VariantUInt.serialise(self.value)
        elif self.variant_type == VariantType.FLOAT:
            value = VariantFloat.serialise(self.value)
        elif self.variant_type == VariantType.STR:
            value = VariantStr.serialise(self.value)
        elif self.variant_type == VariantType.VECTOR2:
            value = VariantVector2.serialise(self.value)
        elif self.variant_type == VariantType.VECTOR3:
            value = VariantVector3.serialise(self.value)

        data.write(value)

        self.data = data

        return data
