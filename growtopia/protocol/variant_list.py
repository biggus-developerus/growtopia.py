__all__ = ("VariantList",)

from typing import Any

from .variant import Variant


class VariantList:
    def __init__(self, *variants: Any) -> None:
        self.variants: list[Variant] = []
        self.__data = bytearray([0])

        for variant in variants:
            self.append(Variant(variant))

    def get(self, index: int) -> Variant:
        return self.variants[index] if index < len(self.variants) else None

    def append(self, variant: Variant) -> None:
        self.__data += variant.serialise(len(self.variants))
        self.variants.append(variant)

    @property
    def data(self) -> bytearray:
        self.__data[0] = len(self.variants)
        return bytes(self.__data)
