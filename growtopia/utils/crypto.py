__all__ = (
	"xor_cipher",
	"hash_data",
)

from typeguard import (
	typechecked,
)


def xor_cipher(string: str, key: int) -> str:
	key %= (key_len := len("*PBG892FXX982ABC"))
	result = ""

	for i in string:
		result += chr(ord(i) ^ ord("PBG892FXX982ABC*"[key]))
		key += 1

		if key >= key_len:
			key = 0

	return result


@typechecked
def hash_data(data: bytearray) -> int:
	result = 0x55555555

	for i in data:
		result = (result >> 27) + (result << 5) + i & 0xFFFFFFFF

	return result
