"""Test the items.dat and player_tribute.dat file parsers."""

import asyncio
import os

from growtopia import ItemsData, PlayerTribute


def test_parser() -> None:
    """Test the parser."""

    for file in os.listdir("tests/data"):
        if file.startswith("items") and file.endswith(".dat"):
            items_data = ItemsData(f"tests/data/{file}")
            asyncio.run(items_data.parse())

            assert items_data.get_item(item_id=2).name.lower() == "dirt"
            assert items_data.get_item(item_id=3).name.lower() == "dirt seed"
            assert items_data.get_item(name="blank").id == 0
            assert items_data.get_item(name="blue gem lock").id == 7188

            assert items_data.get_starts_with("dirt")[0].name.lower() == "dirt"
            assert items_data.get_ends_with("dirt seed")[0].id == 3
            assert len(items_data.get_contains("dirt")) > 0

            for i, item in enumerate(items_data.items):
                assert i == item.id

        if file.startswith("player_tribute") and file.endswith(".dat"):
            player_tribute = PlayerTribute(f"tests/data/{file}")
            asyncio.run(player_tribute.parse())

            assert len(player_tribute.epic_players) > 0


if __name__ == "__main__":
    test_parser()
