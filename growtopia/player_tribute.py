__all__ = ("PlayerTribute",)

from .file import File
from .obj_holder import ObjHolder
from .protocol import GameUpdatePacket, GameUpdatePacketType


class PlayerTribute(File):
    """
    Represents the player_tribute.dat file. Allows for easy access to player tribute data.

    Parameters
    ----------
    data: Union[str, bytes]
        The data to parse. Can be a path to the file or bytes.

    Attributes
    ----------
    content: memoryview
        A memoryview of the raw bytes of the player_tribute.dat file.
    hash: int
        The hash of the player_tribute.dat file.
    epic_players: list[str]
        A list of all the names that are listed as "Epic Players" in the player_tribute.dat file.
    exceptional_mentors: list[str]
        A list of all the names that are listed as "Exceptional Mentors" in the player_tribute.dat file.
    charity_champions: dict[str, list[str]]
        A dictionary that has years as keys and a list of names as values.
    """

    def __init__(self, data: str | bytes) -> None:
        super().__init__(data)

        self.version: int = 0

        self.epic_players: list[str] = []
        self.exceptional_mentors: list[str] = []
        self.charity_champions: list[str] = []

        ObjHolder.player_tribute = self

    def _parse_names(self, names: bytearray) -> list[str]:
        return [name.strip() for name in names.decode("utf-8").split(";")]

    async def parse(self) -> None:
        """
        Parses the file's contents.

        Returns
        -------
        None
        """
        if not self.content:
            await self.read_file()

        offset = 0

        self.epic_players = self._parse_names(
            bytearray(self.content[2 : 2 + int.from_bytes(self.content[:2], "little")])
        )

        offset += 2 + int.from_bytes(self.content[:2], "little")

        # TODO: Parse the rest of the file (Exceptional Mentors and Charity Champions)

        self.hash_file()

    @property
    def packet(self) -> GameUpdatePacket:
        """
        Returns the packet that should be sent to the client when it requests for the player_tribute.dat file.

        Returns
        -------
        GameUpdatePacket
            The packet that should be sent to the client when it requests for the player_tribute.dat file.

        Examples
        --------
        >>> from growtopia import PlayerTribute
        >>> player_tribute = PlayerTribute("player_tribute.dat")
        >>> player_tribute.packet
        """
        if not self.content:
            raise ValueError("The items.dat file has not been read yet.")

        return GameUpdatePacket(
            update_type=GameUpdatePacketType.SEND_PLAYER_TRIBUTE_DATA, extra_data=bytes(self.content)
        )
