__all__ = ("WorldAvatarPool",)

from typing import TYPE_CHECKING, Optional, Callable
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from ..avatar import Avatar


class WorldAvatarPool(ABC):
    """
    Used to store and manage avatars in a world.

    Attributes
    ----------
    avatars: dict[int, Avatar]
        The avatars in the world.
    """

    def __init__(self) -> None:
        self.avatars: dict[int, "Avatar"] = {}

    @property
    @abstractmethod
    def next_net_id(self) -> int:
        ...

    @property
    @abstractmethod
    def spawn_pos(self) -> tuple[int, int]:
        ...

    @abstractmethod
    def lambda_broadcast(self, callback: Callable, exclude_net_id: int = -1) -> None:
        ...

    def add_avatar(self, avatar: "Avatar") -> bool:
        """
        Adds an avatar to the world.

        Parameters
        ----------
        avatar: Avatar
            The avatar to add to the world.

        Returns
        -------
        bool:
            True if the avatar was added, False otherwise.
        """
        if avatar.net_id in self.avatars:
            return False

        if avatar.world == None:
            avatar.world = self

        avatar.net_id = self.next_net_id
        avatar.pos = self.spawn_pos

        self.avatars[avatar.net_id] = avatar

        self.lambda_broadcast(
            lambda player: player._on_spawn(avatar, False),
            exclude_net_id=avatar.net_id,
        )

        self.next_net_id += 1

        return True

    def get_avatar(self, net_id: int) -> Optional["Avatar"]:
        """
        Gets an avatar by their net id.

        Parameters
        ----------
        net_id: int
            The net id of the avatar to get.

        Returns
        -------
        Avatar:
            The avatar with the net id.
        """
        return self.avatars.get(net_id, None)

    def remove_avatar(self, avatar: "Avatar") -> bool:
        """
        Removes an avatar from the world.

        Parameters
        ----------
        avatar: Avatar
            The avatar to remove from the world.

        Returns
        -------
        bool:
            True if the avatar was removed, False otherwise.
        """
        if avatar.net_id not in self.avatars:
            return False

        del self.avatars[avatar.net_id]

        self.lambda_broadcast(lambda p: p._on_remove(avatar), exclude_net_id=avatar.net_id)

        return True
