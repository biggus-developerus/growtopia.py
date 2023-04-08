__all__ = ("decipher",)


def decipher(name: str, key: int) -> str:

    key %= (key_len := len("*PBG892FXX982ABC"))
    result = ""

    for i in name:
        result += chr(ord(i) ^ ord("PBG892FXX982ABC*"[key]))
        key += 1

        if key >= key_len:
            key = 0

    return result
