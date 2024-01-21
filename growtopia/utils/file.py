__all__ = ("File",)

from typing import Union
from abc import ABC
from .buffer import (
    ReadBuffer,
    WriteBuffer,
)
from .proton import (
    decrypt,
    proton_hash,
)


class File(ABC):
    """
    Represents a file, usually items.dat or player_tribute.dat

    Attributes
    ----------
    buffer: `Union[ReadBuffer, WriteBuffer]`
        The file buffer

    Methods
    -------
    is_items_data(path_or_data: `Union[str, memoryview]`) -> `bool`
        Checks if the file is items.dat
    is_player_tribute(path_or_data: `Union[str, memoryview]`) -> `bool`
        Checks if the file is player_tribute.dat
    save(path: `str`) -> `None`
        Saves the file to the specified path
    """

    def __init__(self) -> None:
        self.buffer: Union[ReadBuffer, WriteBuffer]
        self.hash: int

    @staticmethod
    def is_items_data(path_or_data: Union[str, memoryview]) -> bool:
        """
        Checks if the file is items.dat

        Parameters
        ----------
        path_or_data: `Union[str, memoryview]`
            The path or data of the file

        Returns
        -------
        `bool`
            Whether the file is items.dat

        Raises
        ------
        TypeError
            If path_or_data is not str or memoryview

        Examples
        --------
        >>> from growtopia import File
        >>> File.is_items_data("items.dat")
        True
        >>> File.is_items_data("player_tribute.dat")
        False
        """
        if not isinstance(path_or_data, str) and not isinstance(path_or_data, memoryview):
            raise TypeError(f"Expected str or memoryview, got {type(path_or_data)}")

        buff = ReadBuffer.load(path_or_data)
        buff.skip(
            2 + 4 + 8
        )  # version, item count, id, editable_type, category, action_type, hit_sound_type

        return decrypt(buff.read_string(), 0) == "Blank"

    @staticmethod
    def is_player_tribute(path_or_data: Union[str, memoryview]) -> bool:
        """
        Checks if the file is player_tribute.dat

        Parameters
        ----------
        path_or_data: `Union[str, memoryview]`
            The path or data of the file

        Returns
        -------
        `bool`
            Whether the file is player_tribute.dat

        Raises
        ------
        TypeError
            If path_or_data is not str or memoryview

        Examples
        --------
        >>> from growtopia import File
        >>> File.is_player_tribute("player_tribute.dat")
        True
        >>> File.is_player_tribute("items.dat")
        False
        """
        if not isinstance(path_or_data, str) and not isinstance(path_or_data, memoryview):
            raise TypeError(f"Expected str or memoryview, got {type(path_or_data)}")

        raise NotImplementedError("TODO: implement this")

    def _get_hash(self) -> int:
        """
        Gets the hash of the file

        Parameters
        ----------
        None

        Returns
        -------
        `int`
            The hash of the file

        Raises
        ------
        None

        Examples
        --------
        >>> from growtopia import File
        >>> file = File()
        >>> file._get_hash()
        """
        if self.hash:
            return self.hash

        self.hash = proton_hash(self.buffer.data)

        return self.hash

    def save(self, path: str) -> None:
        """
        Saves the file to the specified path

        Parameters
        ----------
        path: `str`
            The path to save the file to

        Returns
        -------
        None

        Raises
        ------
        None

        Examples
        --------
        >>> from growtopia import File
        >>> file = File()
        >>> file.save("items.dat")
        """
        with open(path, "wb") as f:
            f.write(bytes(self.buffer.data))
