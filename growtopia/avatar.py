__all__ = ("Avatar",)

from typing import TYPE_CHECKING, Optional
from .protocol import GameUpdatePacket, VariantList, GameUpdatePacketType

if TYPE_CHECKING:
    from .world import World


class Avatar:
    def __init__(self) -> None:
        self._net_id: int = -1
        self._user_id: int = 0

        self.world: Optional["World"] = None
        self.pos: tuple[float, float] = (0.0, 0.0)

        self.display_name: str = ""
        self.country: str = ""

        self.frozen: bool = False
        self.invisible: bool = False
        self.moderator: bool = False
        self.super_moderator: bool = False

    @property
    def net_id(self) -> int:
        """
        Returns the net ID of the avatar.

        Returns
        -------
        int:
            The net ID of the avatar.
        """
        return self._net_id

    @net_id.setter
    def net_id(self, value: int) -> None:
        """
        Sets the net ID of the avatar.

        Parameters
        ----------
        value: int
            The net ID to set.
        """
        self._net_id = value

    @property
    def user_id(self) -> int:
        """
        Returns the user ID of the avatar.

        Returns
        -------
        int:
            The user ID of the avatar.
        """
        return self._user_id

    @user_id.setter
    def user_id(self, value: int) -> None:
        """
        Sets the user ID of the avatar.

        Parameters
        ----------
        value: int
            The user ID to set.
        """
        self._user_id = value

    def send_to_world(self, world: "World") -> bool:
        """
        Sends the avatar to a world.

        Parameters
        ----------
        world: World
            The world to send the avatar to.
        """
        if self.world:
            self.world.remove_avatar(self)

        self.world = world

        if self.world is None:
            return False

        return self.world.add_avatar(self)

    @property
    def local_packet(self) -> GameUpdatePacket:
        return GameUpdatePacket(
            update_type=GameUpdatePacketType.CALL_FUNCTION,
            variant_list=VariantList(
                "OnSpawn",
                f"spawn|avatar\nnetID|{self.net_id}\nuserID|{self.user_id}\ncolrect|0|0|20|30\nposXY|{self.pos[0]}|{self.pos[1]}\nname|{self.display_name}\ncountry|{self.country}\ninvis|{int(self.invisible)}\nmstate|{int(self.moderator)}\nsmstate|{int(self.super_moderator)}\ntype|local\n",
            ),
        )

    @property
    def packet(self) -> GameUpdatePacket:
        return GameUpdatePacket(
            update_type=GameUpdatePacketType.CALL_FUNCTION,
            variant_list=VariantList(
                "OnSpawn",
                f"spawn|avatar\nnetID|{self.net_id}\nuserID|{self.user_id}\ncolrect|0|0|20|30\nposXY|{self.pos[0]}|{self.pos[1]}\nname|{self.display_name}\ncountry|{self.country}\ninvis|{int(self.invisible)}\nmstate|{int(self.moderator)}\nsmstate|{int(self.super_moderator)}\n",
            ),
        )
