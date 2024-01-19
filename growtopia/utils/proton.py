__all__ = (
    "encrypt",
    "decrypt",
    "proton_hash",
)

# Different functions for encryption and decryption to avoid confusion. (or well having a function name that doesn't make sense)


def encrypt(string: str, key: int) -> str:
    """
    Encrypts a string with a key.

    Parameters
    ----------
    string: `str`
        The string to encrypt.
    key: `int`
        The key to encrypt the string with.

    Returns
    -------
    `str`
        The encrypted string.

    Examples
    --------
    >>> from growtopia.utils import encrypt
    >>> encrypt("Blank", 0)
    """
    key %= (key_len := len("*PBG892FXX982ABC"))
    result = ""

    for i in string:
        result += chr(ord(i) ^ ord("PBG892FXX982ABC*"[key]))
        key += 1

        if key >= key_len:
            key = 0

    return result


def decrypt(string: str, key: int) -> str:
    """
    Decrypts an encrypted string with a key.

    Parameters
    ----------
    string: `str`
        The string to decrypt.
    key: `int`
        The key to decrypt the string with.

    Returns
    -------
    `str`
        The decrypted string.

    Examples
    --------
    >>> from growtopia.utils import decrypt
    >>> decrypt(encrypt("Blank", 0), 0)
    """
    key %= (key_len := len("*PBG892FXX982ABC"))
    result = ""

    for i in string:
        result += chr(ord(i) ^ ord("PBG892FXX982ABC*"[key]))
        key += 1

        if key >= key_len:
            key = 0

    return result


def proton_hash(data: memoryview) -> int:
    """
    Hashes the given data.

    Parameters
    ----------
    data: `memoryview`
        The data to make a hash of.

    Returns
    -------
    `int`
        The hash of the data.

    Examples
    --------
    >>> from growtopia.utils import hash
    >>> data = bytearray([0] * 300)
    >>> proton_hash(memoryview(data)
    """
    result = 0x55555555

    for i in data:
        result = (result >> 27) + (result << 5) + i & 0xFFFFFFFF

    return int(result)
