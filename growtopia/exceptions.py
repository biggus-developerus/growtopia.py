__all__ = (
    "GrowtopiaException",
    "ParserException",
    "UnsupportedItemsData",
)

from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from .items_data import ItemsData
    from .player_tribute import PlayerTribute

    from .protocol import Packet

from .constants import ignored_attributes


class GrowtopiaException(Exception):
    """Base exception class for all exceptions raised by this library."""

    def __init__(self, error_name: str, message: str):
        self.error_name: str = error_name
        self.message: str = message

        super().__init__(
            self.message,
        )

    def __str__(self):
        return f"{self.message}"


class ParserException(GrowtopiaException):
    """An exception that's raised due to a fail in the parse function."""

    def __init__(
        self,
        error_name: str,
        message: str,
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
        )


class PacketException(GrowtopiaException):
    """An exception that's raised when a packet fails to be parsed or appears to be malformed."""

    def __init__(self, error_name: str, message: str, packet: "Packet"):
        self.packet: "Packet" = packet

        super().__init__(
            error_name,
            message,
        )


# Parser Exceptions


class UnsupportedItemsData(ParserException):
    """An exception that's raised when the items.dat file's version appears to be unsupported."""

    def __init__(self, items_data: "ItemsData"):
        error_name = "UnsupportedItemsData"
        message = f"Unsupported items.dat version: {items_data.version}. Supported versions: {list(ignored_attributes.keys())}"

        super().__init__(
            error_name,
            message,
            items_data,
            None,
        )


# Packet Exceptions


class BadPacketLength(PacketException):
    """An exception that's raised when a packet's length is not what it's supposed to be."""

    def __init__(self, packet: "Packet", expected_length: Union[str, int]):
        error_name = "BadPacketLength"
        message = f"Packet length is not what it's supposed to be. Expected: {expected_length}, got: {len(packet.data)}"

        super().__init__(
            error_name,
            message,
            packet,
        )
