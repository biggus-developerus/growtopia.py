__all__ = (
    "VariantInt",
    "VariantUInt",
    "VariantFloat",
    "VariantStr",
    "VariantVector2",
    "VariantVector3",
    "VariantNone",
)


from utils import Buffer


class VariantInt:
    @classmethod
    def serialise(cls, data: int) -> Buffer:
        return Buffer().write_int(data)

    @classmethod
    def deserialise(cls, data: Buffer) -> Buffer:
        return data.read_int()


class VariantUInt:
    @classmethod
    def serialise(cls, data: int) -> Buffer:
        return Buffer().write_int(data)

    @classmethod
    def deserialise(cls, data: Buffer) -> Buffer:
        return data.read_int(data.size)


class VariantFloat:
    @classmethod
    def serialise(cls, data: int) -> Buffer:
        return Buffer().write_float(data)

    @classmethod
    def deserialise(cls, data: Buffer) -> Buffer:
        return data.read_float(data.size)


class VariantStr:
    @classmethod
    def serialise(cls, data: int) -> Buffer:
        return Buffer().write_str(data)

    @classmethod
    def deserialise(cls, data: Buffer) -> Buffer:
        return data.read_str(data.size)


class VariantVector2:
    @classmethod
    def serialise(cls, data: int) -> Buffer:
        return Buffer().write_int(data)

    @classmethod
    def deserialise(cls, data: Buffer) -> Buffer:
        return data.read_int(data.size)


class VariantVector3:
    @classmethod
    def serialise(cls, data: int) -> Buffer:
        return Buffer().write_int(data)

    @classmethod
    def deserialise(cls, data: Buffer) -> Buffer:
        return data.read_int(data.size)


class VariantNone:
    @classmethod
    def serialise(cls) -> Buffer:
        return Buffer()

    @classmethod
    def deserialise(cls) -> Buffer:
        return None
