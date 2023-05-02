__all__ = ("Context",)

from typing import TYPE_CHECKING, Optional

import enet

if TYPE_CHECKING:
    from .server import Server


class Context:
    def __init__(self) -> None:
        ...
