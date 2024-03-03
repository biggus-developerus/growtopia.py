from growtopia import (
    ItemsData,
    disable_logger,
)

disable_logger()


def test_items_data_parser():
    items_data = ItemsData.load("data/items.dat")
    items_data.to_bytes(compress=True).save_to_file("data/compressed_items.dat")

    items_data = ItemsData.load("data/compressed_items.dat", compressed=True)

    for i, item in enumerate(items_data):
        assert i == item.id


if __name__ == "__main__":
    test_items_data_parser()
