from typing import Union

from growtopia import (
    File,
    ItemsData,
    Logger,
    PlayerTribute,
)


def parse_file(path: str) -> None:
    data: Union[ItemsData, PlayerTribute, None] = None

    if File.is_items_data(path):
        data = ItemsData(path)
    # elif File.is_player_tribute(path):
    #     data = PlayerTribute(path)

    if data is None:
        raise ValueError("Unknown file type, must be items.dat or player_tribute.dat")

    data.parse()

    if isinstance(data, PlayerTribute):
        return

def main(*args):
    tool = args[0] if args else None

    match tool:
        case "parse":
            if len(args) < 2:
                raise ValueError("Missing file path")

            parse_file(args[1])
        case "help":
            print(
                """
                growtopia parse <file_path> | Parse a file (items.dat or player_tribute.dat)
                growtopia help | Show this help message
                """
            )


if __name__ == "__main__":
    from sys import argv

    main(*argv[1:] if len(argv) > 1 else [])
