__all__ = (
    "HelloPacket",
    "TextPacket",
    "MessagePacket",
    "UpdatePacket",
)


from ast import literal_eval
from dataclasses import (
    dataclass,
)
from typing import Optional

from utils import Buffer

from .enums import (
    ObjectType,
    PacketFlag,
    PacketType,
    UpdateType,
)
from .variant_list import (
    VariantList,
)


@dataclass
class HelloPacket:
    packet_type: PacketType = PacketType.HELLO

    def serialize(self) -> Buffer:
        data: Buffer = Buffer()

        data.write_int(self.packet_type)

        return data


@dataclass
class TextPacket:
    packet_type: PacketType = PacketType.TEXT
    text: str = ""

    def __init__(self, text: str) -> None:
        self.text = text

    def serialize(self) -> Buffer:
        data: Buffer = Buffer()

        data.write_int(self.packet_type)
        data.write_str(self.text)

        return data

    @classmethod
    def from_bytes(cls, data: Buffer) -> "TextPacket":
        # CHEEECKS
        if data.size < 4:
            raise Exception("PacketTooSmall")

        packet_type = data.read_int()  # type

        if packet_type != PacketType.TEXT:
            raise Exception("PacketNotMatch")

        text = data.read_str(data.size_remaining)  # text

        return cls(text)


@dataclass
class MessagePacket:
    packet_type: PacketType = PacketType.GAME_MESSAGE
    text: str = ""
    action: str = ""
    arguments: dict[str, any] = {}

    def __init__(self, text: str) -> None:
        self.text = text

        _text: list[str] = text.split("\n")

        self.action = _text[0].split("|")[1]
        _text.pop(0)  # Remove the action

        self.arguments: dict[str, any] = {}

        for arg in _text:
            (key, value) = arg.split("|")

            # Type caster
            try:
                value = literal_eval(value)
            except ValueError:
                pass

            self.arguments[key] = value

    def serialize(self) -> Buffer:
        data: Buffer = Buffer()

        data.write_int(self.packet_type)
        data.write_str(self.text)

        return data

    @classmethod
    def from_bytes(cls, data: Buffer) -> "MessagePacket":
        # MORREE checkcs
        if data.size < 4:
            raise Exception("PacketTooSmall")

        packet_type = data.read_int()  # type

        if packet_type != PacketType.GAME_MESSAGE:
            raise Exception("PacketNotMatch")

        text = data.read_str(data.size_remaining)  # text

        return cls(text)


@dataclass
class UpdatePacket:
    packet_type: PacketType = PacketType.GAME_UPDATE
    update_type: UpdateType = UpdateType.UNKNOWN
    object_type: ObjectType = ObjectType.NULL
    count1: int = 0
    count2: int = 0
    net_id: int = -1
    target_net_id: int = 0
    flags: list[PacketFlag] = []
    float_: float = 0.0
    int_: int = 0
    vec_x: float = 0.0
    vec_y: float = 0.0
    velo_x: float = 0.0
    velo_y: float = 0.0
    particle_rotation: float = 0.0
    int_x: int = 0
    int_y: int = 0
    extra_data_size: int = 0
    extra_data: Buffer = Buffer()
    variant_list: Optional[VariantList] = None

    def __init__(self, **kwargs) -> None:
        fields = self.__dataclass_fields__

        for key, value in kwargs.items():
            if key not in fields.keys():
                continue

            if key == "packet_type":
                assert value == PacketType.GAME_UPDATE

            field_type: any = fields[key].type

            if type(value) != field_type:
                raise Exception(
                    f"Incorrect type passed for '{key}', expected {field_type} got {type(value)}"
                )

            fields[key] = value

    def set_variant_list(self, variant_list: VariantList) -> None:
        if PacketFlag.EXTRA_DATA not in self.flags:
            self.flags.append(PacketFlag.EXTRA_DATA)

        self.extra_data = variant_list.serialize()
        self.extra_data_size = len(self.extra_data)

        self.variant_list = variant_list

    def get_variant_list(self) -> Optional[VariantList]:
        if PacketFlag.EXTRA_DATA not in self.flags:
            return None

        if self.variant_list:
            return self.variant_list

        self.variant_list = VariantList(self.extra_data)

        return self.variant_list

    def serialize(self) -> Buffer:
        data: Buffer = Buffer()

        data.write_int(self.packet_type)
        data.write_int(self.update_type)
        data.write_int(self.object_type)

        data.write_int(self.count1)
        data.write_int(self.count2)

        data.write_int(self.net_id)
        data.write_int(self.target_net_id)

        if (PacketFlag.EXTRA_DATA not in self.flags) and self.extra_data:
            self.flags.append(PacketFlag.EXTRA_DATA)

        combined_flags: int = 0
        for flag in self.flags:
            combined_flags |= flag

        data.write_int(combined_flags)

        data.write_float(self.float_)
        data.write_int(self.int_)

        data.write_int(self.vec_x)
        data.write_int(self.vec_y)
        data.write_int(self.velo_x)
        data.write_int(self.velo_y)

        data.write_int(self.particle_rotation)

        data.write_int(self.int_x)
        data.write_int(self.int_y)

        if PacketFlag.EXTRA_DATA in self.flags:
            if self.extra_data_size == 0:
                self.extra_data_size = len(self.extra_data)

            data.write_int(self.extra_data_size)
            data.write(self.extra_data)

        return data

    @classmethod
    def from_bytes(cls, data: Buffer) -> "UpdatePacket":
        kwargs: dict[str, any] = {}

        # bunch of stupid checks fuck me
        if data.size < 4:
            raise Exception("PacketTooSmall")

        packet_type = data.read_int()

        if packet_type != PacketType.GAME_UPDATE:
            raise Exception("PacketDontMatch")

        kwargs["packet_type"] = packet_type  # type

        if data.size < 52:
            raise Exception("PacketTooSmall")

        kwargs["update_type"] = data.read_int(1)  # update_type
        kwargs["object_type"] = data.read_int(1)  # object_type
        kwargs["count1"] = data.read_int(1)  # count1
        kwargs["count2"] = data.read_int(1)  # count2
        kwargs["net_id"] = data.read_int()  # net_id
        kwargs["target_net_id"] = data.read_int()  # target_net_id

        flag_value = data.read_int()
        flags: list[PacketFlag] = []

        if flag_value != 0:
            for flag in PacketFlag:
                if flag_value & flag:
                    if flag not in flags:
                        flags.append(flag)

        kwargs["flags"] = flag_value  # flags

        kwargs["float_"] = data.read_float()  # float
        kwargs["int_"] = data.read_int()  # int
        kwargs["vec_x"] = data.read_int()  # vec_x
        kwargs["vec_y"] = data.read_int()  # vec_y
        kwargs["velo_x"] = data.read_int()  # velo_x
        kwargs["velo_y"] = data.read_int()  # velo_y
        kwargs["particle_rotation"] = data.read_int()  # particle_rotation
        kwargs["int_x"] = data.read_int()  # int_x
        kwargs["int_y"] = data.read_int()  # int_y

        if (PacketFlag.EXTRA_DATA in flags) or (data.size_remaining > 0):
            # making sure it aint fucked up
            if data.size_remaining < 60:
                raise Exception("PacketTooSmall")

            extra_data = data.read(data.size_remaining)

            kwargs["extra_data_size"] = len(extra_data)  # extra_data_size
            kwargs["extra_data"] = extra_data  # extra_data

        return cls(**kwargs)
