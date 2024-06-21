__all__ = (
    "Variant",
    "IntVariant",
    "StrVariant",
    "TYPE_TO_OBJ_MAPPING",
)

from growtopia._types import (
    LengthPrefixedStr,
    Pack,
    TVariant,
    TVariantValue,
    int8,
    int32,
)
from growtopia.net.protocol.enums import (
    VariantType,
)
from growtopia.utils import (
    Packer,
)


class Variant:
    def __init__(
        self, index: int, variant_type: VariantType, variant_value: TVariantValue | None = None
    ) -> None:
        self.index: int = index
        self.variant_type: VariantType = variant_type
        self.variant_value: TVariantValue | None = variant_value

    def get_size(self) -> int:
        if self.variant_type == VariantType.STR:
            return 2 + len(self.variant_value)
        if self.variant_type == VariantType.INT:
            return 6


class IntVariant(Variant, Packer):
    index: Pack[int8]
    variant_type: Pack[int8]
    variant_value: Pack[int32]

    def __init__(self, variant_value: int | None = None) -> None:
        Variant.__init__(self, -1, VariantType.INT, variant_value)

class UIntVariant(Variant, Packer):
    index: Pack[int8]
    variant_type: Pack[int8]
    variant_value: Pack[int32]

    def __init__(self, variant_value: int | None = None) -> None:
        Variant.__init__(self, -1, VariantType.UINT, variant_value)

class FloatVariant(Variant, Packer):
    index: Pack[int8]
    variant_type: Pack[int8]
    variant_value: Pack[float]

    def __init__(self, variant_value: float | None = None) -> None:
        Variant.__init__(self, -1, VariantType.FLOAT, variant_value)

class StrVariant(Variant, Packer):
    index: Pack[int8]
    variant_type: Pack[int8]
    variant_value: Pack[LengthPrefixedStr]

    def __init__(self, variant_value: str | None = None) -> None:
        Variant.__init__(self, -1, VariantType.STR, variant_value)


TYPE_TO_OBJ_MAPPING: dict[VariantType, TVariant] = {
    VariantType.INT: IntVariant,
    VariantType.STR: StrVariant,
}
