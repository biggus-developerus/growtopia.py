__all__ = ("VariantList",)


from typing import (
    Optional,
    Union,
)

from utils import Buffer

from .variant import Variant


class VariantList:
    def __init__(self, *variants: Union[str, int, float, Variant]) -> None:
        self.variants: list[Variant] = []

        for value in variants:
            self.variants.append(Variant(value) if isinstance(value, Variant) else value)

        self.data: Buffer = Buffer()

    def get(self, index: int) -> Optional[Variant]:
        return self.variants[index] if index < len(self.variants) else None

    def add(self, variant: Variant) -> None:
        self.variants.append(variant)

    def serialize(self) -> Buffer:
        data: Buffer = Buffer(bytearray([len(self.variants)]))

        for i, variant in enumerate(self.variants):
            data.write(variant.serialize(i))

        self.data = data

        return data

    def __getitem__(self, i) -> Variant:
        return self.variants[i]

    def __len__(self) -> int:
        return len(self.variants)

    def __iadd__(self, variant: Variant) -> "VariantList":
        self.add(variant)

        return self

    def __add__(self, variant: Variant) -> "VariantList":
        self.add(variant)

        return self
