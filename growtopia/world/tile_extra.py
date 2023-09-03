__all__ = ("TileExtra",)

from .enums import TileExtraDataType


class TileExtra:
    def __init__(self) -> None:
        self.extra_data_type: TileExtraDataType = TileExtraDataType.NONE
        self.extra_data: bytearray = bytearray()

    def reset_extra_data(self) -> None:
        self.extra_data_type = TileExtraDataType.NONE
        self.extra_data = bytearray()

    def _set_door_extra_data(self, door_label: str) -> None:
        self.extra_data_type = TileExtraDataType.DOOR

        self.extra_data += len(door_label).to_bytes(2, "little")
        self.extra_data += door_label.encode()
        self.extra_data += int(0).to_bytes(1, "little")

    def _serialise_extra_data(self) -> bytearray:
        data = bytearray()

        if self.extra_data_type != TileExtraDataType.NONE:
            data += self.extra_data_type.to_bytes(1, "little")
            data += self.extra_data

        return data
