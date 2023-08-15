__all__ = (
    "Command",
    "CommandDec",
)

import asyncio
import inspect

from typing import Callable, Coroutine, Optional, get_type_hints, Union

from .enums import Colour
from .dialog import Dialog, DialogElement
from .context import ServerContext


class InvalidArg:
    """
    Represents an invalid argument that was passed in by the user.

    This is used internally by the Command decorator to check if the user passed in an invalid argument.
    """

    def __init__(self, arg: str, param_name: str, caster: type) -> None:
        self.arg: str = arg
        self.param_name: str = param_name
        self.caster: type = caster


class CommandDec:
    """
    Represents a coroutine function that can be dispatched by an event dispatcher.

    What makes this different from the Listener, is that whenever it is dispatched,
    the arguments will be automatically parsed and passed into the callback.

    An example of that would be:
        >> /give 2 200

        The callback would be called with the arguments: (2, 200)

    An example of a command callback:
        ```py
        @Command(aliases=("get"))
        async def give(self, item_id: int, amount: int):
            # do something with the arguments
        ```

    The arguments passed will also be converted to the type specified in the callback.
    Defaults to str if no type is specified.


    Parameters
    ----------
    callback: Callable
        The coroutine function that will be dispatched.
    name: Optional[str]
        The name of the command. This attribute can either be set manually or automatically by the function's name.
    help_message: Optional[str]
        The help message that will be sent to the user when the player passes invalid arguments.
    aliases: Optional[tuple[str]]
        The alias names that can be used to call the command instead of the command's original name.

    Attributes
    ----------
    name: str
        The name of the command. This attribute can either be set manually or automatically by the function's name.
    help_message: Optional[str]
        The help message that will be sent to the user when the player passes invalid arguments.
    aliases: Optional[tuple[str]]
        The alias names that can be used to call the command instead of the command's original name.
    callback: Callable
        The coroutine function that will be dispatched.
    """

    def __init__(
        self,
        callback: Callable,
        name: Optional[str] = None,
        description: Optional[str] = None,
        help_message: Optional[str] = None,
        aliases: Optional[tuple[str]] = None,
    ) -> None:
        if not asyncio.iscoroutinefunction(callback):
            raise TypeError("Callback must be a coroutine function.")

        self.callback: Callable = callback
        self.name: str = name or callback.__name__
        self.description: Optional[str] = description or "No description provided."
        self.help_message: Optional[Union[str, Dialog]] = help_message
        self.aliases: Optional[tuple[str]] = aliases

        self._belongs_to: object = None
        self._is_dialog_listener: bool = False

        self._hints = get_type_hints(callback)
        self._cmd_params = []  # list[tuple(param_name, param_type, param_default)]
        self._kwarg_name = (
            None
            if callback.__code__.co_kwonlyargcount == 0
            else callback.__code__.co_varnames[callback.__code__.co_argcount]
        )

        self._init_args()

    @property
    def _default_help_message(self) -> Dialog:
        return Dialog(
            name=f"{self.name}_help",
            elements=[
                DialogElement.label_with_icon_big(
                    f"Help ~ {Colour.LIGHT_YELLOW}{self.name}", itemid=1752
                ),  # guest book
                DialogElement.smalltext(f"Usage: /{self.name} {' '.join([param[0] for param in self._cmd_params])}"),
                DialogElement.smalltext(self.description),
                DialogElement.spacer_small(),
                DialogElement.label_with_icon_small("Aliases", itemid=12526),
                DialogElement.smalltext(", ".join(self.aliases) if self.aliases else "None"),
                DialogElement.spacer_small(),
                DialogElement.label_with_icon_small("Parameter types", itemid=12526),
                *[
                    DialogElement.smalltext(f"{param[0]}: {self._hints.get(param[0], str).__name__}")
                    for param in self._cmd_params
                ],
            ],
        )

    def _init_args(self) -> None:
        self._cmd_params = []  # reset the params

        for param_name, param in inspect.signature(self.callback).parameters.items():
            if param.annotation is ServerContext:
                continue

            self._cmd_params.append((param_name, param.annotation, param.default))

        if self._belongs_to:
            self._cmd_params.pop(0)  # remove self

    def _cast_args(self, args_from_text: list[str]) -> list:
        casted_args = []

        for i, arg in enumerate(args_from_text):
            if i >= len(self._cmd_params):
                break

            caster = self._cmd_params[i][1]

            if caster is inspect._empty:
                caster = str

            try:
                casted_args.append(caster(arg))
            except ValueError:
                casted_args.append(InvalidArg(arg, self._cmd_params[i][0], caster))

        return casted_args

    def _parse_args(self, command_args: list[str]) -> dict[str]:
        command_args = self._cast_args(command_args)
        res = {}

        for i, param in enumerate(self._cmd_params):
            res[param[0]] = (
                command_args[i]
                if i < len(command_args)
                else param[2]
                if not param[2] is inspect._empty
                else InvalidArg(None, param[0], param[1])
            )

        return res

    def __call__(self, command_args: list[str], *args, **kwargs) -> Coroutine:
        ctx: ServerContext = args[0]
        command_args: dict[str] = self._parse_args(command_args)

        if any(isinstance(arg, InvalidArg) for arg in command_args.values()):
            if self.help_message:
                if isinstance(self.help_message, Dialog):
                    ctx.player.on_dialog_request(self.help_message)
                else:
                    ctx.player.send_log(self.help_message)

                return None

            ctx.player.on_dialog_request(self._default_help_message)
            return None

        kwargs.update(command_args)

        if self._belongs_to is not None:
            return self.callback(self._belongs_to, *args, **kwargs)

        return self.callback(*args, **kwargs)


def Command(*args, **kwargs) -> Callable:  # wrapper for CommandDec
    """
    Represents a coroutine function that can be dispatched by an event dispatcher.

    What makes this different from the Listener, is that whenever it is dispatched,
    the arguments will be automatically parsed and passed into the callback.

    An example of that would be:
        >> /give 2 200

        The callback would be called with the arguments: (2, 200)

    An example of a command callback:
        ```py
        @Command(aliases=("get"))
        async def give(self, item_id: int, amount: int):
            # do something with the arguments
        ```

    The arguments passed will also be converted to the type specified in the callback.
    Defaults to str if no type is specified.


    Parameters
    ----------
    callback: Callable
        The coroutine function that will be dispatched.
    name: Optional[str]
        The name of the command. This attribute can either be set manually or automatically by the function's name.
    help_message: Optional[str]
        The help message that will be sent to the user when the player passes invalid arguments.
    aliases: Optional[tuple[str]]
        The alias names that can be used to call the command instead of the command's original name.

    Attributes
    ----------
    name: str
        The name of the command. This attribute can either be set manually or automatically by the function's name.
    help_message: Optional[str]
        The help message that will be sent to the user when the player passes invalid arguments.
    aliases: Optional[tuple[str]]
        The alias names that can be used to call the command instead of the command's original name.
    callback: Callable
        The coroutine function that will be dispatched.
    """

    def wrapper(callback) -> CommandDec:
        if isinstance(callback, list):
            raise TypeError("A list was passed in instead of a callback. Did you forget to call the Command decorator?")

        return CommandDec(callback, *args, **kwargs)

    return wrapper
