__all__ = ("Tile",)


class Tile:
    def __init__(self, *, foreground: int = 0, background: int = 0) -> None:
        self.foreground: int = foreground
        self.background: int = background

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
        """
        Creates a tile from bytes.

        Parameters
        ----------
        data: bytes
            The bytes to create the tile from.

        Returns
        -------
        Tile:
            The tile.
        """
        tile = cls()

        tile.foreground = int.from_bytes(data[:2], "little")
        tile.background = int.from_bytes(data[2:4], "little")

        tile.lockpos = int.from_bytes(data[4:6], "little")
        tile.flags = int.from_bytes(data[6:8], "little")

        if tile.flags != 0:  # TODO: Obviously handle the extra data.. 😢
            tile.extra_type = int.from_bytes(data[8:9], "little")
            tile.extra_data = data[9:]

        return tile
