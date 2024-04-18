import pytest

from struct import pack, unpack
from os import chdir, path
from dataclasses import dataclass
from growtopia import Packer
from growtopia._types import *
from typing import TypeVar

chdir(path.abspath(path.dirname(__file__)))


class TestStruct(Packer):
    __test__ = False

    int8_value: Pack[int8]
    str_value: Pack[LengthPrefixedStr]
    int_value: Pack[int32]
    float_value: Pack[float]

    def __init__(self) -> None:
        self.int8_value: int = None
        self.str_value: str = None
        self.int_value: int = None
        self.float_value: float = None

T = TypeVar("T")
@dataclass
class TestStruct2(Packer):
    __test__ = False

    unknown_type: Pack[T]

@dataclass
class TestOptional(Packer):
    __test__ = False

    non_opt: Pack[int32]
    optional_int: OptionalPack[int32] = None
    optional_int2: OptionalPack[int8] = None
    
def test_packer() -> None:
    int8_value = 100
    str_value = "hi"
    int_value = 69
    float_value = 69.69

    data = bytearray()
    data += int8_value.to_bytes(1, "little")
    data += len(str_value.encode()).to_bytes(2, "little")
    data += str_value.encode()
    data += int_value.to_bytes(4, "little")
    data += pack("f", float_value)

    test_struct: TestStruct = TestStruct()
    
    assert test_struct.str_value == None and test_struct.int_value == None and test_struct.int8_value == None and test_struct.float_value == None
    assert test_struct.unpack(data)
    assert test_struct.str_value == str_value and test_struct.int_value == int_value and int(float_value) == int(test_struct.float_value)
    assert test_struct.pack() == data
    assert test_struct.unpack(data[:-1]) == False

    with pytest.raises(ValueError):
        TestStruct2(69)

    with pytest.raises(ValueError):
        TestOptional(None, None).pack()

    data = bytearray(b'\x01\x00\x00\x002\x00\x00\x00')
    data2 = bytearray(b'\x01\x00\x00\x00')

    opt1_test = TestOptional.from_bytes(data, None)
    opt2_test = TestOptional.from_bytes(data2, None)

    assert opt1_test.non_opt == 1 and opt1_test.optional_int == 50 and opt1_test.optional_int2 == None
    assert opt2_test.non_opt == 1 and opt2_test.optional_int == None and opt2_test.optional_int2 == None


if __name__ == "__main__":
    test_packer()
