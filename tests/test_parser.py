"""Test the item.dat and player_tribute.dat file parser."""


import growtopia


def test_parser() -> None:
    """Test the parser."""

    items_data = growtopia.ItemsData("tests/data/items_v14.dat")
    player_tribute = growtopia.PlayerTribute("tests/data/player_tribute.dat")

    growtopia.extensions.parse(items_data, player_tribute)

    assert items_data.get_item(item_id=2).name.lower() == "dirt"
    assert items_data.get_item(item_id=3).name.lower() == "dirt seed"
    assert items_data.get_item(name="blank").id == 0
    assert items_data.get_item(name="blue gem lock").id == 7188

    assert items_data.get_starts_with("dirt")[0].name.lower() == "dirt"
    assert items_data.get_ends_with("dirt seed")[0].id == 3
    assert len(items_data.get_contains("dirt")) > 0


if __name__ == "__main__":
    test_parser()
