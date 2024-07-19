from os import chdir, path

import growtopia

chdir(path.abspath(path.dirname(__file__)))


def test_protocol() -> None:
    packet = growtopia.Packet(growtopia.PacketType.HELLO)
    assert packet.pack() == bytearray(b"\x01\x00\x00\x00")

    packet = growtopia.StrPacket(growtopia.PacketType.TEXT, "action|msg\nlog|xd\n")
    assert packet.pack() == bytearray(b"\x02\x00\x00\x00action|msg\nlog|xd\n")

    packet = growtopia.StrPacket(growtopia.PacketType.MSG, "action|msg\nlog|xd\n")
    assert packet.pack() == bytearray(b"\x03\x00\x00\x00action|msg\nlog|xd\n")

    size = packet.unpack(bytearray(b"\x03\x00\x00\x00action|msg\nlog|xd\n"))
    assert size == 22


if __name__ == "__main__":
    test_protocol()
