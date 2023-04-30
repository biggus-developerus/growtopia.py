__all__ = ("PlayerTribute",)

from typing import BinaryIO, Union

from .file import File


class PlayerTribute(File):
    """
    Represents the player_tribute.dat file. Allows for easy access to player tribute data.

    Parameters
    ----------
    data: Union[str, bytes, BinaryIO]
        The data to parse. Can be a path to the file, bytes, or, a file-like object.

    Attributes
    ----------
    content: bytes
        The raw bytes of the player_tribute.dat file.
    hash: int
        The hash of the player_tribute.dat file.
    """

    def __init__(self, data: Union[str, bytes, BinaryIO]) -> None:
        super().__init__(data)

    def parse(self) -> None:
        """
        Parses the contents passed into the initialiser.

        Returns
        -------
        None
        """
        self.hash_file()
