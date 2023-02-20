from growtopia.items_data import ItemsData
from growtopia.player_tribute import PlayerTribute

def decipher(name: str, key: int) -> str:
    """
    Deciphers a ciphered item name using its id.
    Parameters
    -----------
    name: :class:`str`
        The ciphered item name.
    key: :class:`int`
        The item's id.
    Returns
    --------
    :class:`str`
        The deciphered item name.
    """

def hash_(data: bytes) -> int:
    """
    Hashes the contents of a file.
    Parameters
    -----------
    data: :class:`bytes`
        The contents of the file to be hashed.
    Returns
    --------
    :class:`int`
        The hash of the file.
    """

def parse(items_data: ItemsData = None, player_tribute: PlayerTribute = None) -> None:
    """
    Parses the items.dat and player_tribute.dat files.
    Parameters
    -----------
    items_data: :class:`ItemsData`
        An :class:`ItemsData` object. Will be ignored if not provided.
    player_tribute: :class:`PlayerTribute`
        A :class:`PlayerTribute` object. Will be ignored if not provided.
    Returns
    --------
    :class:`None`
    """
