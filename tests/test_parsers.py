from asyncio import run
from os import chdir, path

import pytest

from growtopia import (
    ItemsData,
)

chdir(path.abspath(path.dirname(__file__)))


@pytest.mark.asyncio
async def test_items_data_parser():
    items_data = ItemsData.load(
        ItemsData.load("data/items.dat").to_bytes(compress=True).data,
        compressed=True,
    )

    for i, item in enumerate(items_data.items):
        assert i == item.id


if __name__ == "__main__":
    run(test_items_data_parser())
