__all__ = ("WorldObjectPool",)

from .world_object import WorldObject


class WorldObjectPool:
    def __init__(self) -> None:
        self.objects: list[WorldObject] = []
