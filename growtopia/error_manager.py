__all__ = ("ErrorManager",)

from typing import Callable, Optional


class ErrorManager:
    callback: Optional[Callable] = None

    @classmethod
    def set_callback(cls, callback: Callable) -> None:
        cls.callback = callback

    @classmethod
    def _raise_exception(cls, exception: Exception) -> None:
        if cls.callback is not None:
            cls.callback(exception)
        else:
            raise exception
