__all__ = ("TypeEnforcerMeta",)

from typing import (
    Any,
    Tuple,
    Type,
)


class TypeEnforcerMeta(type):
    def __call__(cls, *args, **kwargs) -> Any:
        enforcing_type: Type = getattr(cls, "enforcing_type", None)
        enforcing_for: Tuple[Type, ...] = getattr(cls, "enforcing_for", ())

        if not enforcing_type:
            return super().__call__(*args, **kwargs)

        new_args = [enforcing_type(arg) if isinstance(arg, enforcing_for) else arg for arg in args]

        new_kwargs = {
            key: enforcing_type(value) if isinstance(value, enforcing_for) else value
            for key, value in kwargs.items()
        }

        return super().__call__(*new_args, **new_kwargs)
