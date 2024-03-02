__all__ = ("TBytesLike",)

from typing import TypeVar

TBytesLike = TypeVar("TBytesLike", bound=bytes)
