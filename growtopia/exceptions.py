from __future__ import annotations

__all__ = (
    "GrowtopiaException",
    "ParserException",
    "PacketException",
    "UnsupportedItemsData",
    "PacketTypeDoesNotMatchContent",
    "PacketTooSmall",
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .items_data import ItemsData
    from .player_tribute import PlayerTribute
    from .protocol import Packet, StrPacket, PacketType

from .constants import ignored_attributes

# Exceptions that are raised by growtopia.py.
# These exceptions can be checked for when handling errors.
# For example:
# try:
#     ...
# except UnsupportedItemsData as e: | or GrowtopiaException to catch all exceptions
#     print(e.version)


class GrowtopiaException(Exception):
    """
    Base exception class for all exceptions raised by this library.
    This exception can be caught to handle all exceptions raised by this library.

    Parameters
    ----------
    error_name: str
            The name of the error.
    message: str
            The message of the error.

    Attributes
    ----------
    error_name: str
            The name of the error.
    message: str
            The message of the error.
    """

    def __init__(self, error_name: str, message: str):
        self.error_name: str = error_name
        self.message: str = message

        super().__init__(
            self.message,
        )

    def __str__(self):
        return f"{self.error_name}: {self.message}"


class PacketException(GrowtopiaException):
    """
    An exception that's raised due to a fail in the Packet's child class.
    This exception can be caught to handle all packet exceptions.

    Parameters
    ----------
    error_name: str
            The name of the error.
    message: str
            The message of the error.
    packet: Optional[Union[Packet, StrPacket]]
            The Packet object that was being handled when the error occurred.

    Attributes
    ----------
    packet: Optional[Packet]
            The Packet object that was being handled when the error occurred.
    """

    def __init__(self, error_name: str, message: str, packet: "Packet" | "StrPacket" | None = None):
        self.packet: "Packet" | "StrPacket" = packet
        super().__init__(error_name, message)


class ParserException(GrowtopiaException):
    """
    An exception that's raised due to a fail in a file's parser.
    This exception can be caught to handle all parser exceptions.

    Parameters
    ----------
    error_name: str
            The name of the error.
    message: str
            The message of the error.
    items_data: Optional[ItemsData]
            The ItemsData object that was being parsed when the error occurred.
    player_tribute: Optional[PlayerTribute]
            The PlayerTribute object that was being parsed when the error occurred.

    Attributes
    ----------
    items_data: Optional[ItemsData]
            The ItemsData object that was being parsed when the error occurred.
    player_tribute: Optional[PlayerTribute]
            The PlayerTribute object that was being parsed when the error occurred.
    version: Optional[int]
            The version of the items.dat file.
    supported_versions: list[int]
            A list of all the supported versions of the items.dat file.
    """

    def __init__(
        self,
        error_name: str,
        message: str,
        items_data: "ItemsData" | None = None,
        player_tribute: "PlayerTribute" | None = None,
    ):
        self.items_data: "ItemsData" | None = items_data or None
        self.player_tribute: "PlayerTribute" | None = player_tribute or None
        self.version: int | None = items_data.version if items_data else None
        self.supported_versions: list[int] = list(ignored_attributes.keys())

        super().__init__(
            error_name,
            message,
        )


# Parser Exceptions


class UnsupportedItemsData(ParserException):
    """
    An exception that's raised when the items.dat file's version appears to be unsupported.

    Parameters
    ----------
    items_data: ItemsData
            The ItemsData object that was being parsed when the error occurred.

    Attributes
    ----------
    items_data: ItemsData
            The ItemsData object that was being parsed when the error occurred.
    version: int
            The version of the items.dat file.
    supported_versions: list[int]
            A list of all the supported versions of the items.dat file.
    """

    def __init__(self, items_data: "ItemsData"):
        error_name = "UnsupportedItemsData"
        message = f"Unsupported items.dat version: {items_data.version}. Supported versions: {list(ignored_attributes.keys())}"

        super().__init__(
            error_name,
            message,
            items_data,
            None,
        )


class PacketTypeDoesNotMatchContent(PacketException):
    """
    An exception that's raised when the Packet being handled does not match the content of the Packet.

    Parameters
    ----------
    packet: Packet
            The Packet object that was being handled when the error occurred.

    Attributes
    ----------
    packet: Packet
            The Packet object that was being handled when the error occurred.
    """

    def __init__(self, packet: "Packet" | "StrPacket", packet_type_from_content: "PacketType"):
        error_name = "PacketTypeDoesNotMatchContent"
        message = f"Packet type does not match content. Packet type: {packet._type}, packet type from content: {packet_type_from_content}"

        super().__init__(
            error_name,
            message,
            packet,
        )


class PacketTooSmall(PacketException):
    """
    An exception that's raised when the Packet being handled is less than 4 bytes.

    Parameters
    packet: Packet
            The Packet object that was being handled when the error occurred.

    Attributes
    ----------
    packet: Packet
            The Packet object that was being handled when the error occurred.
    """

    def __init__(self, packet: "Packet" | "StrPacket", data_length: int, size_required: str = ">=4"):
        error_name = "PacketTooSmall"
        message = f"Packet is too small, required length: {size_required}, got: {data_length}"

        super().__init__(
            error_name,
            message,
            packet,
        )
