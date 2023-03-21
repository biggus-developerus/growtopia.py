from ..constants import ignored_attributes
from ..exceptions import UnsupportedItemsData
from ..item import Item
from ..items_data import ItemsData
from ..player_tribute import PlayerTribute


def decipher(name, key):
    key %= len("*PBG892FXX982ABC")
    result = ""

    for i in name:
        result += chr(ord(i) ^ ord("PBG892FXX982ABC*"[key]))
        key += 1

        if key >= len("PBG892FXX982ABC*"):
            key = 0

    return result


def hash_(data):
    result = 0x55555555

    for i in data:
        result = (result >> 27) + (result << 5) + i & 0xFFFFFFFF

    return int(result)


def parse(items_data=None, player_tribute=None):
    if items_data:
        if not isinstance(items_data, ItemsData):
            raise TypeError("items_data must be an instance of ItemsData")

        data, offset = items_data.content, 6

        items_data.version = int.from_bytes(data[:2], "little")
        items_data.item_count = int.from_bytes(data[2:6], "little")

        if (
            items_data.version < list(ignored_attributes.keys())[0]
            or items_data.version > list(ignored_attributes.keys())[-1]
        ):
            raise UnsupportedItemsData(items_data)

        for i in range(items_data.item_count):
            item = Item()

            for attr in item.__dict__:
                if attr in ignored_attributes[items_data.version]:
                    continue

                if isinstance(item.__dict__[attr], int):
                    size = item.__dict__[attr]
                    item.__dict__[attr] = int.from_bytes(
                        data[offset : offset + size], "little"
                    )
                    if attr == "break_hits":
                        item.__dict__[attr] = item.__dict__[attr] / 6
                    offset += size
                elif isinstance(item.__dict__[attr], str):
                    str_len = int.from_bytes(data[offset : offset + 2], "little")
                    offset += 2

                    if attr == "name":
                        item.__dict__[attr] = decipher(
                            "".join(chr(i) for i in data[offset : offset + str_len]),
                            item.id,
                        )
                    else:
                        item.__dict__[attr] = "".join(
                            chr(i) for i in data[offset : offset + str_len]
                        )

                    offset += str_len

                elif isinstance(item.__dict__[attr], bytearray):
                    item.__dict__[attr] = data[
                        offset : offset + len(item.__dict__[attr])
                    ]
                    offset += len(item.__dict__[attr])

            items_data.items[item.id] = item

        items_data.hash = hash_(data)

    if player_tribute is not None:
        if not isinstance(player_tribute, PlayerTribute):
            raise TypeError("player_tribute must be an instance of PlayerTribute")

        player_tribute.hash = hash_(player_tribute.content)
