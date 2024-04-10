__all__ = ("ItemsData",)

from typing import (
	Iterator,
	List,
	Optional,
	Union,
)

from typeguard import (
	typechecked,
)

from ..utils import (
	LOG_LEVEL_INFO,
	Buffer,
	CompressionType,
	hash_data,
	log,
)
from .constants import (
	LATEST_ITEMS_DATA_VERSION,
)
from .item import Item


class ItemsData:
	__slots__ = ("version", "hash", "items")

	def __init__(self, version: Optional[int], items: Optional[List[Item]]) -> None:
		self.version: int = version or 0
		self.hash: int = 0
		self.items: List[Item] = items or []

	@staticmethod
	@typechecked
	def load(
			path_or_bytes: Union[str, bytearray],
			*,
			compressed: bool = False,
			compression_type: CompressionType = CompressionType.ZLIB,
	) -> "ItemsData":
		buffer = Buffer.load(path_or_bytes)

		if compressed:
			buffer.decompress(compression_type)

		items_data = ItemsData(
			buffer.read_int(2),
			[Item.from_bytes(buffer, LATEST_ITEMS_DATA_VERSION) for _ in range(buffer.read_int())],
		)

		items_data.set_hash()

		log(
			LOG_LEVEL_INFO,
			f"Loaded {path_or_bytes if isinstance(path_or_bytes, str) else 'items data'} file | {items_data}",
		)

		return items_data

	def to_bytes(
			self,
			*,
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

		log(LOG_LEVEL_INFO, f"Serialised items data | {self}")

		return buffer

	def set_hash(self, data: Optional[bytearray] = None) -> int:
		self.hash = hash_data(data or self.to_bytes().data)

	def __str__(self) -> str:
		return f"<ItemsData: version={self.version}, hash={self.hash}, items={len(self.items)}>"

	def __getitem__(self, index: int) -> "Item":
		return self.items[index]

	def __iter__(self) -> Iterator[Item]:
		return iter(self.items)

	def __len__(self) -> int:
		return len(self.items)
