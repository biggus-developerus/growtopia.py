__all__ = ("CommandObject", "Command")


from asyncio import (
    iscoroutinefunction,
)
from typing import (
    Callable,
    Optional,
    Union,
)

from dialog import Dialog


class CommandObject:
    def __init__(
        self,
        callback: Callable,
        name: Optional[str] = None,
        description: Optional[str] = "...",
        help_message: Optional[str] = "...",
        aliases: Optional[tuple[str]] = [],
    ) -> None:
        if not iscoroutinefunction(callback):
            raise Exception("Callback must be a coroutine function.")

        self.callback: Callable = callback
        self.name: str = name or callback.__name__
        self.description: str = description
        self.help_message: Union[str, Dialog] = help_message
        self.aliases: tuple[str] = aliases

        self.origin: Optional[object] = None
        self.is_origin_dialog: bool = False

        self.params: list[tuple[str, any, any]] = []
        self._biggius_bullshit = (
            None
            if callback.__code__.co_kwonlyargcount == 0
            else callback.__code__.co_varnames[callback.__code__.co_argcount]
        )

        self._init_args()
