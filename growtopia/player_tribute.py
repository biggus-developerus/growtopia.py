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
    epic_players: list[str]
        A list of all the names that are listed as "Epic Players" in the player_tribute.dat file.
    exceptional_mentors: list[str]
        A list of all the names that are listed as "Exceptional Mentors" in the player_tribute.dat file.
    charity_champions: dict[str, list[str]]
        A dictionary that has years as keys and a list of names as values.
    """

    def __init__(self, data: Union[str, bytes, BinaryIO]) -> None:
        super().__init__(data)

        self.version: int = 0

        self.epic_players: list[str] = []
        self.exceptional_mentors: list[str] = []
        self.charity_champions: list[str] = []

    def _parse_names(self, names: bytearray) -> list[str]:
        return [name.strip() for name in names.decode("utf-8").split(";")]

    def parse(self) -> None:
        """
        Parses the contents passed into the initialiser.

        Returns
        -------
        None
        """

        offset = 0

        self.epic_players = self._parse_names(
            bytearray(self.content[2 : 2 + int.from_bytes(self.content[:2], "little")])
        )

        offset += 2 + int.from_bytes(self.content[:2], "little")

        # TODO: Parse the rest of the file (Exceptional Mentors and Charity Champions)

        self.hash_file()
