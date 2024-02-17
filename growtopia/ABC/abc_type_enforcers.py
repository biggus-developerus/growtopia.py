__all__ = ("TypeEnforcerMVBytesLike",)

from typing import Tuple, Type

from ..meta import (
    TypeEnforcerMeta,
)


class TypeEnforcerMVBytesLike(metaclass=TypeEnforcerMeta):
    enforcing_type: Type[memoryview] = memoryview
    enforcing_for: Tuple[Type, ...] = (bytes, bytearray)

    def __new__(cls, *args, **kwargs) -> "TypeEnforcerMVBytesLike":
        if cls is TypeEnforcerMVBytesLike:
            raise TypeError("Cannot instantiate TypeEnforcerMVBytesLike directly")

        return super().__new__(cls)
