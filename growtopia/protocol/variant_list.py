__all__ = ("VariantList",)

from typing import Any

from .variant import Variant


class VariantList:
    def __init__(self, *variants: Any) -> None:
        self.variants: list[Variant] = []
        self.data = bytearray([0])

        for variant in variants:
            self.append(Variant(variant))

    def get(self, index: int) -> Variant:
        return self.variants[index] if index < len(self.variants) else None

    def append(self, variant: Variant) -> None:
        self.data += variant.serialise(len(self.variants))
        self.variants.append(variant)

    def serialise(self) -> bytearray:
        self.data[0] = len(self.variants)
        return bytes(self.data)

    @classmethod
    def from_bytes(cls, data: bytearray) -> "VariantList":
        variant_list, offset = cls(), 1  # Skip the variant count (1 byte)

        for i in range(int.from_bytes(data[0:1], "little")):
            variant_list.append(variant := Variant.from_bytes(data[offset:]))
            offset += len(variant.serialise(i))

        return variant_list

    def __getitem__(self, i) -> Variant:  # allows for indexing
        return self.variants[i]

    def __len__(self) -> int:  # allows for len()
        return len(self.variants)
