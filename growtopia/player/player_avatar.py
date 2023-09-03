__all__ = ("PlayerAvatar",)

from ..avatar import Avatar
from ..world import World


class PlayerAvatar(Avatar):
    def __init__(self) -> None:
        super().__init__()

    def send_to_world(self, world: "World") -> bool:
        """
        Sends the player to a world.

        Parameters
        ----------
        world: World
            The world to send the player to.
        """
        if self.world:
            self.world.remove_player(self)

        self.world = world

        if self.world is None:
            return False

        return self.world.add_player(self)
