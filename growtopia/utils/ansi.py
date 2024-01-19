__all__ = (
    "AnsiESC",
    "AnsiStr",
)

from aenum import Flag

from ..constants import (
    ANSI_ESCAPE
)


class AnsiESC(Flag):
    NONE = 0
    BOLD = 1 << 0
    UNDERLINE = 1 << 1
    REVERSE = 1 << 2
    INVISIBLE = 1 << 3

    RED = 1 << 4
    GREEN = 1 << 5
    YELLOW = 1 << 6
    BLUE = 1 << 7

    def has(self, ansi: "AnsiESC") -> bool:
        return bool(self & ansi)

    def get_params(self) -> list[str]:
        params = []

        for ansi in AnsiESC:
            if self.has(ansi):
                params.append(str(ANSI_ESCAPE[ansi.name.lower()]))

        return params


class AnsiStr(str):
    def wrap(self, *parameters: AnsiESC) -> "AnsiStr":
        combined = AnsiESC(0)

        for param in parameters:
            combined |= param

        return AnsiStr(f"\033[{';'.join(combined.get_params())}m{self}\033[0m")
