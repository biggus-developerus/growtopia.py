__all__ = ("Tile",)


class Tile:
    def __init__(self, *, foreground: int = 0, background: int = 0) -> None:
        self.unknown: int = 0  # uint32
        self.unknown2: int = 0  # uint8

        self.foreground: int = foreground  # uint16
        self.background: int = background  # uint16

        self.lockpos: int = 0  # uint16
        self.flags: int = 0  # uint16
        self.extra_type: int = 0  # uint8
        self.extra_data: bytes = b""

    def serialise(self) -> bytearray:
        """
        Serialises the tile.

        Returns
        -------
        bytearray:
            The serialised world.
        """
        data = bytearray()

        data += self.foreground.to_bytes(2, "little")
        data += self.background.to_bytes(2, "little")

        data += self.lockpos.to_bytes(2, "little")
        data += self.flags.to_bytes(2, "little")

        if self.flags != 0:
            data += self.extra_type.to_bytes(1, "little")
            data += self.extra_data

        return data

    @classmethod
    def from_bytes(cls, data: bytes) -> "Tile":
        raise NotImplementedError
