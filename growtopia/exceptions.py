__all__ = (
    "GrowtopiaException",
    "ParserException",
    "UnsupportedItemsData",
)

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .items_data import ItemsData
    from .player_tribute import PlayerTribute

from .constants import ignored_attributes


class GrowtopiaException(Exception):
    """Base exception class for all exceptions raised by this library."""

    def __init__(
        self, error_name: str, message: str, detailed_message: Optional[str] = None
    ):
        self.error_name: str = error_name
        self.message: str = message
        self.detailed_message: Optional[str] = (
            detailed_message if detailed_message is not None else None
        )

        super().__init__(
            self.message,
        )

    def __str__(self):
        return self.message


class ParserException(GrowtopiaException):
    """An exception that's raised due to a fail in the :function:`parse` function."""

    def __init__(
        self,
        error_name: str,
        message: str,
        detailed_message: Optional[str] = None,
        items_data: Optional["ItemsData"] = None,
        player_tribute: Optional["PlayerTribute"] = None,
    ):
        self.items_data: Optional["ItemsData"] = (
            items_data if items_data is not None else None
        )
        self.player_tribute: Optional["PlayerTribute"] = (
            player_tribute if player_tribute is not None else None
        )

        self.version: Optional[int] = (
            items_data.version if items_data is not None else None
        )
        self.supported_versions: list[int] = list(ignored_attributes.keys())

        super().__init__(
            error_name,
            message,
            detailed_message,
        )


# Parser Exceptions


class UnsupportedItemsData(ParserException):
    """An exception that's raised when the items.dat file's version appears to be unsupported."""

    def __init__(self, items_data: "ItemsData"):
        error_name = "UnsupportedItemsData"
        message = f"Unsupported items.dat version: {items_data.version}. Supported versions: {list(ignored_attributes.keys())}"
        detailed_message = None

        super().__init__(
            error_name,
            message,
            detailed_message,
            items_data,
            None,
        )
