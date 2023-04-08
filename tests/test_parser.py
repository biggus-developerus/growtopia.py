"""Test the items.dat and player_tribute.dat file parsers."""


from growtopia import ItemsData, PlayerTribute


def test_parser() -> None:
    """Test the parser."""

    items_data = ItemsData("tests/data/items_v14.dat")
    player_tribute = PlayerTribute("tests/data/player_tribute.dat")

    items_data.parse()
    player_tribute.parse()

    assert items_data.get_item(item_id=2).name.lower() == "dirt"
    assert items_data.get_item(item_id=3).name.lower() == "dirt seed"
    assert items_data.get_item(name="blank").id == 0
    assert items_data.get_item(name="blue gem lock").id == 7188

    assert items_data.get_starts_with("dirt")[0].name.lower() == "dirt"
    assert items_data.get_ends_with("dirt seed")[0].id == 3
    assert len(items_data.get_contains("dirt")) > 0


if __name__ == "__main__":
    test_parser()
