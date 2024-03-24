from asyncio import run
from os import chdir, path
from json import dump

import pytest

from growtopia import (
    ItemsData,
)

chdir(path.abspath(path.dirname(__file__)))


def find_flags(combined_flags):
    result = []
    flag = 1
    while combined_flags:
        if combined_flags & 1:
            result.append(flag)
        flag <<= 1
        combined_flags >>= 1
    return result


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
