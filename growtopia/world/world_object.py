__all__ = ("WorldObject",)

import struct


class WorldObject:
    def __init__(self) -> None:
        self.id: int = 0  # uint16
        self.pos: tuple[float, float] = (0.0, 0.0)
        self.count: int = 0  # uint8
        self.flags: int = 0  # uint8
        self.object_id: int = 0  # uint32

        self.data: bytearray = bytearray()

    def serialise(self) -> bytearray:
        """
        Serialises the world object.

        Returns
        -------
        bytearray:
            The serialised world object.
        """
        self.data = bytearray()

        self.data += self.id.to_bytes(2, "little")
        self.data += struct.pack("ff", *self.pos)
        self.data += self.count.to_bytes(1, "little")
        self.data += self.flags.to_bytes(1, "little")
        self.data += self.object_id.to_bytes(4, "little")

        return self.data

    @classmethod
    def from_bytes(cls, data: bytes) -> "WorldObject":
        """
        Creates a world object from bytes.

        Parameters
        ----------
        data: bytes
            The bytes to create the world object from.

        Returns
        -------
        WorldObject:
            The world object.
        """
        obj = cls()

        obj.id, obj.pos, obj.count, obj.flags, obj.object_id = struct.unpack("<HffBBi", data[:16])

        return obj
