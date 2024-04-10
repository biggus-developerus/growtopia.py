__all__ = ("ItemPetInfo",)

from dataclasses import (
	dataclass,
)

from ..utils import Buffer


@dataclass
class ItemPetInfo:
	name: str = ""
	name: str = ""
	prefix: str = ""
	suffix: str = ""
	ability: str = ""

	@staticmethod
	def from_bytes(data: Buffer) -> "ItemPetInfo":
		return ItemPetInfo(
			data.read_str(data.read_int(2)),
			data.read_str(data.read_int(2)),
			data.read_str(data.read_int(2)),
			data.read_str(data.read_int(2)),
		)

	def to_bytes(self, buffer: Buffer) -> None:
		buffer.write_int(len(self.name.encode()), 2)
		buffer.write_str(self.name)
		buffer.write_int(len(self.prefix.encode()), 2)
		buffer.write_str(self.prefix)
		buffer.write_int(len(self.suffix.encode()), 2)
		buffer.write_str(self.suffix)
		buffer.write_int(len(self.ability.encode()), 2)
		buffer.write_str(self.ability)
