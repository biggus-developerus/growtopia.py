__all__ = ("ItemsData",)

from typing import (
    Iterator,
    List,
    Union,
)

from typeguard import (
    typechecked,
)

from ..types import TBytesLike
from ..utils import (
    Buffer,
    CompressionType,
    Logger,
    LogLevel,
    hash_data,
)
from .item import Item

LATEST_ITEMS_DATA_VERSION: int = 16


class ItemsData:
    def __init__(self) -> None:
        self.buffer: Buffer = Buffer()

        self.version: int = 0
        self.hash: int = 0
        self.items: List[Item] = []

    @staticmethod
    @typechecked
    def load(
        path_or_bytes: Union[str, TBytesLike],
        is_compressed: bool = False,
        compression_type: CompressionType = CompressionType.ZLIB,
    ) -> "ItemsData":
        buffer = Buffer.load(path_or_bytes)

        items_data = ItemsData()

        if is_compressed:
            buffer.decompress(compression_type)

        items_data.version = buffer.read_int(2)
        items_data.items = [
            Item.from_bytes(buffer, LATEST_ITEMS_DATA_VERSION) for _ in range(buffer.read_int())
        ]
        items_data.hash = hash_data(buffer.data)

        buffer._offset = 0
        items_data.buffer = buffer

        Logger.log(
            f"Loaded {path_or_bytes if isinstance(path_or_bytes, str) else 'items data'} file | {items_data}",
            LogLevel.INFO,
        )

        Logger.wait_until_flushed()

        return items_data

    def to_bytes(
        self,
        compress: bool = False,
        compression_type: CompressionType = CompressionType.ZLIB,
    ) -> Buffer:
        buffer = Buffer()
        buffer.write_int(self.version, 2)
        buffer.write_int(len(self.items), 4)

        for item in self.items:
            item.to_bytes(buffer, LATEST_ITEMS_DATA_VERSION)

        if compress:
            buffer.compress(compression_type)

        Logger.log(
            f"Serialised items data | {self}",
            LogLevel.INFO,
        )

        Logger.wait_until_flushed()

        return buffer

    def __str__(self) -> str:
        return f"<ItemsData: version={self.version}, hash={self.hash}, items={len(self.items)}>"

    def __getitem__(self, index: int) -> "Item":
        return self.items[index]

    def __iter__(self) -> Iterator[Item]:
        return iter(self.items)
