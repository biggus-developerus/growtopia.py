from typing import Optional

from ..items_data import ItemsData
from ..player_tribute import PlayerTribute

def decipher(name: str, key: int) -> str:
    """
    Deciphers a ciphered item name using its id.

    Parameters
    -----------
    name: `str`
        The ciphered item name.
    key: `int`
        The item's id.

    Returns
    --------
    `str`
        The deciphered item name.
    """

def hash_(data: bytes) -> int:
    """
    Hashes the contents of a file.

    Parameters
    -----------
    data: `bytes`
        The contents of the file to be hashed.

    Returns
    --------
    `int`
        The hash of the file.
    """

def parse(items_data: ItemsData = None, player_tribute: PlayerTribute = None) -> None:
    """
    Parses the items.dat and player_tribute.dat files.

    Parameters
    -----------
    items_data: `Optional[ItemsData]`
        An `ItemsData` object. Will be ignored if not provided.
    player_tribute: `Optional[PlayerTribute]`
        A `PlayerTribute` object. Will be ignored if not provided.

    Returns
    --------
    `None`
    """
