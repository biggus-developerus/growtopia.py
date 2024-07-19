from os import chdir, path

import growtopia

chdir(path.abspath(path.dirname(__file__)))


def test_protocol() -> None:
    packet = growtopia.Packet(growtopia.PacketType.HELLO)
    assert packet.pack() == bytearray(b"\x01\x00\x00\x00")

    packet = growtopia.StrPacket(growtopia.PacketType.TEXT, "action|log\nmsg|xd\n")
    assert packet.pack() == bytearray(b"\x02\x00\x00\x00action|log\nmsg|xd\n")

    packet = growtopia.StrPacket(growtopia.PacketType.MSG, "action|log\nmsg|xd\n")
    assert packet.pack() == bytearray(b"\x03\x00\x00\x00action|log\nmsg|xd\n")

    size = packet.unpack(bytearray(b"\x03\x00\x00\x00action|log\nmsg|xd\n"))
    assert size == 22

    assert growtopia.TextPacket.from_mapping({"action": "log"}).text == "action|log\n"
    assert packet.get_mapping() == {"action": "log", "msg": "xd"}

    packet = growtopia.UpdatePacket()
    assert packet.unpack(packet.pack()) == len(packet.pack())

if __name__ == "__main__":
    test_protocol()
