from asyncio import run

from growtopia import (
	ItemsData,
)


def parse_file(path: str) -> None:
	items_data = ItemsData.load(path)


async def main(*args):
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

	run(main(*argv[1:] if len(argv) > 1 else []))
