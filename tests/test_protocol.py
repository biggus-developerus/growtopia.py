from os import chdir, path

import growtopia

chdir(path.abspath(path.dirname(__file__)))


def test_protocol() -> None:
    packet = growtopia.Packet(growtopia.PacketType.HELLO)
    assert (data := packet.pack()) and data == bytearray([1, 0, 0, 0])

    packet = growtopia.StrPacket(growtopia.PacketType.TEXT, "action|log\nmsg|xd\n")
    assert (data := packet.pack()) and data == (bytearray([2, 0, 0, 0]) + b"action|log\nmsg|xd\n")

    packet = growtopia.TextPacket("action|log\nmsg|xd\n")
    assert (data := packet.pack()) and data == (bytearray([2, 0, 0, 0]) + b"action|log\nmsg|xd\n")

    packet = growtopia.MsgPacket("action|log\nmsg|xd\n")
    assert (data := packet.pack()) and data == (bytearray([3, 0, 0, 0]) + b"action|log\nmsg|xd\n")
    assert packet.get_mapping() == {"action": "log", "msg": "xd"}

    packet = growtopia.UpdatePacket(int_y=1)
    assert (
        (data := packet.pack())
        and data
        == bytearray(
            b"\x04\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00"
        )
        and len(data) == 56
    )

    packet = growtopia.TextPacket.from_mapping(
        {"requestedName": "xd", "tankIDName": "xd2", "tankIDPass": "xd3"}
    )
    assert packet.get_mapping() == {"requestedName": "xd", "tankIDName": "xd2", "tankIDPass": "xd3"}
    assert packet.text == "\n".join([f"{k}|{v}\n" for k, v in packet.get_mapping().items()])

    packet = growtopia.UpdatePacket()
    packet.set_variant_list(growtopia.IntVariant(5), growtopia.StrVariant("HI!"))

    vars = packet.get_variant_list()

    assert len(vars) == 2
    assert vars[0].index == 0 and vars[0].variant_type == growtopia.VariantType.INT and vars[0].variant_value == 5
    assert vars[1].index == 1 and vars[1].variant_type == growtopia.VariantType.STR and vars[1].variant_value == "HI!"

if __name__ == "__main__":
    test_protocol()
