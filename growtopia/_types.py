__all__ = (
    "Pack",
    "OptionalPack",
    "LengthPrefixedStr",
    "AllStr",
    "AllData",
    "int8",
    "int16",
    "int32",
)

from typing import (
    Generic,
    TypeVar,
)

LengthPrefixedStr = TypeVar("LengthPrefixedStr", bound=str)
LengthPrefixedData = TypeVar("LengthPrefixedData", bytes, bytearray)
AllStr = TypeVar("AllStr", bound=str)
AllData = TypeVar("AllData", bytes, bytearray)
int8 = TypeVar("int8", bound=int)
int16 = TypeVar("int16", bound=int)
int32 = TypeVar("int32", bound=int)

T = TypeVar("T")


class Pack(Generic[T]):
    pass


class OptionalPack(Generic[T]):
    pass
