__all__ = ("VariantList",)

from .variant import Variant


class VariantList:
    """
    This class is used to store, serialise, and deserialise Variants.

    Parameters
    ----------
    *variants: Union[str, int, float]
        The list of variant values to initialise the VariantList with.

    Attributes
    ----------
    variants: list[Variant]
        The list of variants.
    data: bytearray
        The serialised data. This is updated every time a Variant object is appended.
    """

    def __init__(self, *variants: str | int | float | Variant) -> None:
        self.variants: list[Variant] = [
            Variant(variant) if not isinstance(variant, Variant) else variant for variant in variants
        ]
        self.data = bytearray([0])

    def get(self, index: int) -> Variant | None:
        return self.variants[index] if index < len(self.variants) else None

    def append(self, variant: Variant) -> None:
        self.variants.append(variant)

    def serialise(self) -> bytearray:
        self.data = bytearray([len(self.variants)])

        for i, variant in enumerate(self.variants):
            self.data += variant.serialise(i)

        return self.data

    @classmethod
    def from_bytes(cls, data: bytearray) -> "VariantList":
        variant_list, offset = cls(), 1  # Skip the variant count (1 byte)

        for i in range(int.from_bytes(data[0:1], "little")):
            variant_list.append(variant := Variant.from_bytes(data[offset:]))
            offset += len(variant.serialise(i))

        return variant_list

    def __getitem__(self, i) -> Variant:
        return self.variants[i]

    def __len__(self) -> int:
        return len(self.variants)

    def __iadd__(self, variant: Variant) -> "VariantList":
        self.variants.append(variant)
        return self

    def __add__(self, variant: Variant) -> "VariantList":
        self.variants.append(variant)
        return self
