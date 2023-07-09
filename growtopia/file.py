__all__ = ("File",)

from typing import Union

import aiofiles


class File:
    """
    Represents a file. Allows for easy access and safe access to file data.
    This class is mainly used as a base class for other file classes, such as ItemsData and PlayerTribute.

    Parameters
    ----------
    data: Union[str, bytes, BinaryIO]
        The data to keep hold of, can be a path to the file, bytes, or a file-like object.

    Attributes
    ----------
    content: memoryview
        A memoryview of the raw bytes of the file.

    Raises
    ------
    ValueError
        Invalid data type passed into initialiser.

    Examples
    --------
    >>> from growtopia import File
    >>> file = File("items.dat")
    """

    def __init__(self, data: Union[str, bytes]) -> None:
        self.__content: bytearray = bytearray()
        self.__path: str = ""

        self.hash: int = 0

        if isinstance(data, str):
            self.__path = data
        elif isinstance(data, bytes):
            self.__content = bytearray(data)
        elif isinstance(data, bytearray):
            self.__content = data
        else:
            raise ValueError("Invalid data type passed into initialiser.")

    async def read_file(self) -> None:
        """
        Reads the file and stores the data in memory.

        Examples
        --------
        >>> from growtopia import File
        >>> file = File("items.dat")
        >>> await file.read_file()
        """
        async with aiofiles.open(self.__path, "rb") as f:
            self.__content = bytearray(await f.read())

    @property
    def content(self) -> memoryview:
        """
        A memoryview of the raw bytes of the file.

        Returns
        -------
        memoryview - A memoryview of the raw bytes of the file.

        Examples
        --------
        >>> from growtopia import File
        >>> file = File("items.dat")
        >>> file.content
        """
        return memoryview(self.__content)

    def hash_file(self) -> int:
        """
        Generates a hash based on the contents of the file.

        Returns
        -------
        result: int
            The hash of the file.

        Examples
        --------
        >>> from growtopia import File
        >>> file = File("items.dat")
        >>> file.hash_file()
        """
        result = 0x55555555

        for i in self.content:
            result = (result >> 27) + (result << 5) + i & 0xFFFFFFFF

        self.hash = result

        return int(result)
