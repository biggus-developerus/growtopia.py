__all__ = (
    "AnsiESC",
    "AnsiStr",
)

from aenum import Flag

from ..constants import (
    ANSI_ESCAPE,
)


class AnsiESC(Flag):
    """
    ANSI escape flags.

    Methods
    -------
    has(ansi: AnsiESC) -> bool
        Checks if the flag has the given ANSI escape flag.

    get_params() -> list[str]
        Gets the ANSI escape parameters.
    """

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
        """
        Checks if the flag has the given ANSI escape flag.

        Parameters
        ----------
        ansi: AnsiESC
            The ANSI escape flag to check.

        Returns
        -------
        bool
            Whether the flag has the given ANSI escape flag.

        Raises
        ------
        None

        Examples
        --------
        >>> ansi = AnsiESC.RED | AnsiESC.BOLD
        >>> ansi.has(AnsiESC.RED)
        True
        """
        return bool(self & ansi)

    def get_params(self) -> list[str]:
        """
        Gets the ANSI escape parameters.

        Parameters
        ----------
        None

        Returns
        -------
        list[str]
            The ANSI escape parameters.

        Raises
        ------
        None

        Examples
        --------
        >>> ansi = AnsiESC.RED | AnsiESC.BOLD
        >>> ansi.get_params()
        ["31", "1"]
        """
        params = []

        for ansi in AnsiESC:
            if self.has(ansi):
                params.append(ANSI_ESCAPE[ansi.name.lower()])

        return params


class AnsiStr(str):
    """
    Represents a string with ANSI escape codes. Inherits from `str`.

    Methods
    -------
    wrap(*parameters: AnsiESC, should_reset: bool = True) -> AnsiStr
        Wraps the string with the given ANSI escape codes.

    clear() -> AnsiStr
        Returns the string with the ANSI escape code to clear the screen.
    """

    def wrap(self, *parameters: AnsiESC, should_reset: bool = True) -> "AnsiStr":
        """
        Wraps the string with the given ANSI escape codes.

        Parameters
        ----------
        *parameters: AnsiESC
            The ANSI escape codes to wrap the string with.

        should_reset: bool = True
            Whether to reset the ANSI escape codes after wrapping the string.

        Returns
        -------
        AnsiStr
            The wrapped string.

        Raises
        ------
        None

        Examples
        --------
        >>> ansi_str = AnsiStr("Hello, world!")
        >>> ansi_str.wrap(AnsiESC.RED, AnsiESC.BOLD)
        "\033[31;1mHello, world!\033[0m"
        """
        combined = AnsiESC(0)

        for param in parameters:
            combined |= param

        reset = f"\033[{ANSI_ESCAPE['reset']}m" if should_reset else ""
        return AnsiStr(f"\033[{';'.join(combined.get_params())}m{self}{reset}")

    @staticmethod
    def clear() -> "AnsiStr":
        """
        Returns the string with the ANSI escape code to clear the screen.

        Parameters
        ----------
        None

        Returns
        -------
        AnsiStr
            The string with the ANSI escape code to clear the screen.

        Raises
        ------
        None

        Examples
        --------
        >>> AnsiStr.clear()
        "\033c"
        """
        return AnsiStr(f"\033{ANSI_ESCAPE['clear']}")
