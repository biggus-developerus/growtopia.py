__all__ = (
    "ReadBuffer",
    "WriteBuffer",
)

from typing import Union


class BuffBase:
    """
    The base class for ReadBuffer and WriteBuffer.
    """

    def __len__(self) -> int:
        raise NotImplementedError

    def __bool__(self) -> bool:
        raise NotImplementedError

    def __getitem__(self, _: int) -> int:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<Buffer size={len(self)}>"

    def __str__(self) -> str:
        return repr(self)


class ReadBuffer(BuffBase):
    """
    ReadBuffer class, used to read data from a memoryview.

    Attributes
    ----------
    data: `memoryview`
        The data to read from

    offset: `int`
        The offset of the buffer

    Methods
    -------
    skip(size: `int`) -> `None`
        Skips the given amount of bytes

    get_chunk(start: `int`, end: `int`) -> `ReadBuffer`
        Returns a new ReadBuffer instance with the given chunk

    get_bytes(start: `int`, end: `int`) -> `bytes`
        Returns the bytes of the given chunk

    read_bytes(size: `int`) -> `bytes`
        Reads the given amount of bytes

    read_int(int_size: `int` = 4) -> `int`
        Reads an integer of the given size

    read_string(length_int_size: `int` = 2) -> `str`
        Reads a string, including the integer used to denote the length of the string

    load_file(path: `str`) -> `ReadBuffer`
        Loads a file into a ReadBuffer

    load_bytes(data: `Union[bytes, bytearray]`) -> `ReadBuffer`
        Loads bytes into a ReadBuffer

    load(pbm: `Union[str, bytes, memoryview]`) -> `ReadBuffer`
        Loads a file or bytes into a ReadBuffer
    """

    def __init__(self, data: memoryview) -> None:
        """
        Parameters
        ----------
        data: `memoryview`
            The data to read from

        Raises
        ------
        TypeError
            If the given data is not a memoryview

        Returns
        -------
        None

        Examples
        --------
        >>> ReadBuffer(memoryview(b"hello"))
        <Buffer size=5>
        """
        if not isinstance(data, memoryview):
            raise TypeError(f"Expected memoryview, got {type(data)}")

        self.data: memoryview = data.toreadonly() if not data.readonly else data
        self.offset: int = 0

    def skip(self, size: int) -> None:
        """
        Skips the given amount of bytes.

        Parameters
        ----------
        size: `int`
            The amount of bytes to skip

        Returns
        -------
        None

        Raises
        ------
        None

        Examples
        --------
        >>> buffer = ReadBuffer(memoryview(b"hello"))
        >>> buffer.skip(2)
        >>> buffer.offset
        2
        """
        self.offset += size

    def get_chunk(self, start: int, end: int) -> "ReadBuffer":
        """
        Gets a chunk of the buffer.

        Parameters
        ----------
        start: `int`
            The start of the chunk

        end: `int`
            The end of the chunk

        Returns
        -------
        ReadBuffer
            The chunk

        Raises
        ------
        None

        Examples
        --------
        >>> buffer = ReadBuffer(memoryview(b"hello"))
        >>> buffer.get_chunk(1, 3)
        <Buffer size=2>
        """
        return ReadBuffer(self.data[start:end])

    def get_bytes(self, start: int, end: int) -> bytes:
        """
        Gets the bytes of a chunk of the buffer.

        Parameters
        ----------
        start: `int`
            The start of the chunk

        end: `int`
            The end of the chunk

        Returns
        -------
        bytes
            The bytes of the chunk

        Raises
        ------
        None

        Examples
        --------
        >>> buffer = ReadBuffer(memoryview(b"hello"))
        >>> buffer.get_bytes(1, 3)
        b"el"
        """
        return self.get_chunk(start, end).data.tobytes()

    def read_bytes(self, size: int) -> bytes:
        """
        Reads the given amount of bytes.

        Parameters
        ----------
        size: `int`
            The amount of bytes to read

        Returns
        -------
        bytes
            The bytes read

        Raises
        ------
        None

        Examples
        --------
        >>> buffer = ReadBuffer(memoryview(b"hello"))
        >>> buffer.read_bytes(2)
        b"he"
        """
        value = self.get_bytes(self.offset, self.offset + size)
        self.offset += size

        return value

    def read_int(self, int_size: int = 4) -> int:
        """
        Reads an integer of the given size.

        Parameters
        ----------
        int_size: `int`
            The size of the integer to read

        Returns
        -------
        int
            The integer read

        Raises
        ------
        None

        Examples
        --------
        >>> buffer = ReadBuffer(memoryview(bytearray([1, 0])))
        >>> buffer.read_int(2)
        1
        """
        value = int.from_bytes(self.get_bytes(self.offset, self.offset + int_size), "little")
        self.offset += int_size

        return value

    def read_string(self, length_int_size: int = 2) -> str:
        """
        Reads a string, including the integer used to denote the length of the string.

        Parameters
        ----------
        length_int_size: `int`
            The size of the integer used to denote the length of the string

        Returns
        -------
        str
            The string read

        Raises
        ------
        None

        Examples
        --------
        >>> buffer = ReadBuffer(memoryview(b"\x05\x00hello"))
        >>> buffer.read_string(2)
        "hello"
        """
        length = self.read_int(length_int_size)
        value = "".join(chr(i) for i in self.get_bytes(self.offset, self.offset + length))

        self.offset += length

        return value

    def __len__(self) -> int:
        return len(self.data)

    def __bool__(self) -> bool:
        return bool(self.data)

    def __getitem__(self, index: int) -> int:
        return self.data[index]

    @staticmethod
    def load_file(path: str) -> "ReadBuffer":
        """
        Loads a file into a ReadBuffer.

        Parameters
        ----------
        path: `str`
            The path to the file

        Returns
        -------
        ReadBuffer
            The ReadBuffer instance

        Raises
        ------
        None

        Examples
        --------
        >>> ReadBuffer.load_file("hello.txt")
        <Buffer size=5>
        """
        with open(path, "rb") as file:
            return ReadBuffer(memoryview(file.read()))

    @staticmethod
    def load_bytes(data: Union[bytes, bytearray]) -> "ReadBuffer":
        """
        Loads bytes into a ReadBuffer.

        Parameters
        ----------
        data: `Union[bytes, bytearray]`
            The bytes to load

        Returns
        -------
        ReadBuffer
            The ReadBuffer instance

        Raises
        ------
        None

        Examples
        --------
        >>> ReadBuffer.load_bytes(b"hello")
        <Buffer size=5>
        """
        return ReadBuffer(memoryview(data))

    @staticmethod  # PBM = Path, Bytes, Memoryview
    def load(pbm: Union[str, bytes, memoryview]) -> "ReadBuffer":
        """
        Loads a file or bytes into a ReadBuffer.

        Parameters
        ----------
        pbm: `Union[str, bytes, memoryview]`
            The file path, bytes or memoryview to load

        Returns
        -------
        ReadBuffer
            The ReadBuffer instance

        Raises
        ------
        TypeError
            If the given type is not str, bytes or memoryview

        Examples
        --------
        >>> ReadBuffer.load("hello.txt") or ReadBuffer.load(b"hello") or ReadBuffer.load(memoryview(b"hello"))
        <Buffer size=5>
        """
        if isinstance(pbm, str):
            return ReadBuffer.load_file(pbm)
        elif isinstance(pbm, (bytes, bytearray)):
            return ReadBuffer.load_bytes(pbm)
        elif isinstance(pbm, memoryview):
            return ReadBuffer(pbm)
        else:
            raise TypeError(f"Unknown type: {type(pbm)}, expected str, bytes or memoryview")


class WriteBuffer(BuffBase):
    """
    WriteBuffer class, used to write data to a bytearray.

    Attributes
    ----------
    data: `memoryview`
        A memoryview of the data being written

    Methods
    -------
    write_bytes(data: `bytes`) -> `None`
        Writes the given bytes

    write_int(value: `int`, int_size: `int` = 4) -> `None`
        Writes an integer of the given size

    write_string(value: `str`, length_int_size: `int` = 2) -> `None`
        Writes a string, including the integer used to denote the length of the string
    """

    def __init__(self) -> None:
        """
        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        None

        Examples
        --------
        >>> WriteBuffer()
        <Buffer size=0>
        """
        self.__data: bytearray = bytearray()

    def write_bytes(self, data: bytes) -> None:
        """
        Writes the given bytes.

        Parameters
        ----------
        data: `bytes`
            The bytes to write

        Returns
        -------
        None

        Raises
        ------
        None

        Examples
        --------
        >>> buffer = WriteBuffer()
        >>> buffer.write_bytes(b"hello")
        >>> bytes(buffer.data)
        b"hello"
        """
        self.__data += data

    def write_int(self, value: int, int_size: int = 4) -> None:
        """
        Writes an integer of the given size.

        Parameters
        ----------
        value: `int`
            The integer to write

        int_size: `int`
            The size of the integer to write

        Returns
        -------
        None

        Raises
        ------
        None

        Examples
        --------
        >>> buffer = WriteBuffer()
        >>> buffer.write_int(1, 2)
        >>> bytes(buffer.data)
        b"\x01\x00"
        """
        self.write_bytes(value.to_bytes(int_size, "little"))

    def write_string(self, value: str, length_int_size: int = 2) -> None:
        """
        Writes a string, including the integer used to denote the length of the string.

        Parameters
        ----------
        value: `str`
            The string to write

        length_int_size: `int`
            The size of the integer used to denote the length of the string

        Returns
        -------
        None

        Raises
        ------
        None

        Examples
        --------
        >>> buffer = WriteBuffer()
        >>> buffer.write_string("hello", 2)
        >>> bytes(buffer.data)
        b"\x05\x00hello"
        """
        encoded_value = value.encode()

        self.write_int(len(encoded_value), length_int_size)
        self.write_bytes(encoded_value)

    @property
    def data(self) -> memoryview:
        return memoryview(self.__data).toreadonly()

    def __len__(self) -> int:
        return len(self.__data)

    def __bool__(self) -> bool:
        return bool(self.__data)

    def __getitem__(self, index: int) -> int:
        return self.__data[index]

    def __setitem__(self, index: int, value: int) -> None:
        self.__data[index] = value
