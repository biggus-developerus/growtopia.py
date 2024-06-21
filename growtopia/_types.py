__all__ = (
    "Pack",
    "OptionalPack",
    "LengthPrefixedStr",
    "AllStr",
    "AllData",
    "int8",
    "int16",
    "int32",
    "TVariantValue",
    "TVariant",
)

from typing import (
    TYPE_CHECKING,
    Generic,
    TypeVar,
)

if TYPE_CHECKING:
    from growtopia.net.protocol.variant import (
        FloatVariant,
        IntVariant,
        StrVariant,
        UIntVariant,
    )

type LengthPrefixedStr = str
type LengthPrefixedData = bytes | bytearray
type AllStr = str
type AllData = bytes | bytearray
type int8 = int
type int16 = int
type int32 = int
type TVariantValue = int | str
type TVariant = IntVariant | UIntVariant | FloatVariant | StrVariant

T = TypeVar("T")


class Pack(Generic[T]):
    pass


class OptionalPack(Generic[T]):
    pass
