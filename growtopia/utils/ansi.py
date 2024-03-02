__all__ = (
    "AnsiESC",
    "AnsiStr",
)

from aenum import Flag

ANSI_ESCAPE: dict[str, str] = {
    "bold": "1",
    "underline": "4",
    "reverse": "7",
    "invisible": "8",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "reset": "0",
    "clear": "c",
}


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
                params.append(ANSI_ESCAPE[ansi.name.lower()])

        return params


class AnsiStr(str):
    def wrap(self, *parameters: AnsiESC, should_reset: bool = True) -> "AnsiStr":
        combined = AnsiESC(0)

        for param in parameters:
            combined |= param

        reset = f"\033[{ANSI_ESCAPE['reset']}m" if should_reset else ""
        return AnsiStr(f"\033[{';'.join(combined.get_params())}m{self}{reset}")

    @staticmethod
    def clear() -> "AnsiStr":
        return AnsiStr(f"\033{ANSI_ESCAPE['clear']}")
