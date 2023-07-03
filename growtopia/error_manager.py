__all__ = ("ErrorManager",)

import traceback
from typing import Callable, Optional


class ErrorManager:
    callback: Optional[Callable] = None
    catch_exceptions: bool = True

    @classmethod
    def set_callback(cls, callback: Callable) -> None:
        cls.callback = callback

    @classmethod
    def _raise_exception(cls, exception: Exception) -> None:
        if cls.callback is not None:
            return cls.callback(exception)

        # We catch the exception here to prevent the program from halting.
        # Traceback is still printed out due to the print_exc() call.
        if cls.catch_exceptions:
            try:
                raise exception
            except Exception:
                traceback.print_exc()  # Print the traceback to the console
        else:
            raise exception
