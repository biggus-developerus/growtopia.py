__all__ = (
    "encrypt",
    "decrypt",
    "proton_hash",
)

# Different functions for encryption and decryption to avoid confusion
# or well having a function name that doesn't make sense


def encrypt(string: str, key: int) -> str:
    key %= (key_len := len("*PBG892FXX982ABC"))
    result = ""

    for i in string:
        result += chr(ord(i) ^ ord("PBG892FXX982ABC*"[key]))
        key += 1

        if key >= key_len:
            key = 0

    return result


def decrypt(string: str, key: int) -> str:
    key %= (key_len := len("*PBG892FXX982ABC"))
    result = ""

    for i in string:
        result += chr(ord(i) ^ ord("PBG892FXX982ABC*"[key]))
        key += 1

        if key >= key_len:
            key = 0

    return result


def proton_hash(data: memoryview) -> int:
    result = 0x55555555

    for i in data:
        result = (result >> 27) + (result << 5) + i & 0xFFFFFFFF

    return int(result)
