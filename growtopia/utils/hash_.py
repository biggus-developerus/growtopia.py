__all__ = ("hash_",)


def hash_(data: bytes) -> int:
    result = 0x55555555

    for i in data:
        result = (result >> 27) + (result << 5) + i & 0xFFFFFFFF

    return int(result)
