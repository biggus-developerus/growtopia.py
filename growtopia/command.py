__all__ = ("Command",)

import asyncio
from typing import Callable, Coroutine, get_type_hints

# TODO: Allow users to pass aliases for the command name and a help message for the command.
# TODO: Allow users to have optional (with default values) arguments for the command.

# The alias name would be used to call the command instead of the function's name.
# The help message would be sent to the user when the player passes invalid arguments.

# An example of the above would be:
# command = Command(callback, aliases=("give", "gift"), help="Usage: /give <item_id> <amount>")


class Command:
    """
    Represents a coroutine function that can be dispatched by an event dispatcher.

    What makes this different from the Listener, is that whenever it is dispatched,
    the arguments will be automatically parsed and passed into the callback.

    An example of that would be:
        >> /give 2 200

        The callback would be called with the arguments: (2, 200)

    An example of a command callback:
        ```py
        @Command
        async def give(self, item_id: int, amount: int):
            # do something with the arguments
        ```

    The arguments passed will also be converted to the type specified in the callback.
    Defaults to str if no type is specified.


    Parameters
    ----------
    callback: Callable
        The coroutine function that will be dispatched.

    Attributes
    ----------
    name: str
        The name of the command. This attribute can either be set manually or automatically by the function's name.
    callback: Callable
        The coroutine function that will be dispatched.
    """

    def __init__(self, callback: Callable) -> None:
        if not asyncio.iscoroutinefunction(callback):
            raise TypeError("Callback must be a coroutine function.")

        self.name: str = callback.__name__
        self.callback: Callable = callback

        self._belongs_to: object = None
        self._is_dialog_listener: bool = False

        self._hints = get_type_hints(callback)
        self._cmd_args = {}

        self._init_args()  # this will be called twice if the command is in a Collection

    def _init_args(self) -> None:
        self._cmd_args.clear()  # reset cmd args (in case the command is in a Collection and needs to get rid of the second arg as well (ctx))

        varnames = self.callback.__code__.co_varnames[
            2 if self._belongs_to is not None else 1 :
        ]  # get rid of self and Context

        for arg in varnames:
            self._cmd_args[arg] = self._hints.get(arg, str)

    def _parse_args(self, command_args: list[str]) -> list:
        args_from_text = []

        for arg in command_args:
            if len(args_from_text) == (len(self._cmd_args) - 1) and self.callback.__code__.co_kwonlyargcount != 0:
                args_from_text.append(" ".join(command_args[len(args_from_text) :]))
                break

            args_from_text.append(arg)

        return args_from_text

    def __call__(self, command_args: list[str], *args) -> Coroutine:
        kwargs = {}
        cmd_args = self._parse_args(command_args)

        for index, cmd_arg in enumerate(cmd_args):
            kwargs[list(self._cmd_args.keys())[index]] = self._cmd_args[list(self._cmd_args.keys())[index]](cmd_arg)

        if self._belongs_to is not None:
            return self.callback(self._belongs_to, *args, **kwargs)

        return self.callback(*args, **kwargs)
