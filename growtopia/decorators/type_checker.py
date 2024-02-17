__all__ = ("type_checker",)

from inspect import (
    Parameter,
    signature,
)
from typing import (
    Any,
    Callable,
)

# bro don't even ask about the typehinting go figure this shit out yourself (idek what I wrote here)


def type_checker(func: Callable[..., Any]) -> Callable[..., Any]:
    func_sig = signature(func)

    def wrapper(*args, **kwargs) -> Any:
        bound_args = func_sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        for param_name, param in func_sig.parameters.items():
            val, annotation = bound_args.arguments[param_name], param.annotation

            if annotation == Parameter.empty:
                continue

            if not isinstance(val, annotation):
                raise TypeError(
                    f"Argument '{param_name}' must be of type '{annotation}', got '{type(val).__name__}' instead."
                )

        return func(*args, **kwargs)

    return wrapper
