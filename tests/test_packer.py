from os import chdir, path

from growtopia import Packer
from growtopia._types import *

chdir(path.abspath(path.dirname(__file__)))


class TestStruct(Packer):
    __test__ = False

    int8_value: Pack[int8]
    str_value: Pack[LengthPrefixedStr]
    int_value: Pack[int32]

    def __init__(self) -> None:
        self.int8_value: int = None
        self.str_value: str = None
        self.int_value: int = None


def test_packer() -> None:
    int8_value = 100
    str_value = "hi"
    int_value = 69

    data = bytearray()
    data += int8_value.to_bytes(1, "little")
    data += len(str_value.encode()).to_bytes(2, "little")
    data += str_value.encode()
    data += int_value.to_bytes(4, "little")

    test_struct: TestStruct = TestStruct()
    
    assert test_struct.str_value == None and test_struct.int_value == None and test_struct.int8_value == None
    test_struct.unpack(data)
    assert test_struct.str_value == str_value and test_struct.int_value == int_value
    assert test_struct.pack() == data
    assert test_struct.unpack(data[:-1]) == False


if __name__ == "__main__":
    test_packer()
