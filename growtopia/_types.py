__all__ = (
    "Pack",
    "OptionalPack",
    "LengthPrefixedStr",
    "AllStr",
    "AllData",
    "int8",
    "int16",
    "int32",
    "TVariant",
)

from typing import (
    Generic,
    TypeVar,
    TYPE_CHECKING
)

if TYPE_CHECKING:
    from growtopia.net.protocol.variant import Variant

type LengthPrefixedStr = str
type LengthPrefixedData = bytes | bytearray
type AllStr = str
type AllData = bytes | bytearray
type int8 = int
type int16 = int
type int32 = int
type TVariant = int | float | str | tuple | Variant

T = TypeVar("T")
class Pack(Generic[T]):
    pass


class OptionalPack(Generic[T]):
    pass
