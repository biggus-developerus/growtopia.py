import growtopia

from os import chdir, path

chdir(path.abspath(path.dirname(__file__)))

    
def test_protocol() -> None:
    packet = growtopia.Packet(growtopia.PacketType.HELLO)
    assert (data:=packet.pack()) and data == bytearray([1, 0, 0, 0])

    packet = growtopia.StrPacket(growtopia.PacketType.TEXT, "action|log\nmsg|xd\n")
    assert (data:=packet.pack()) and data == (bytearray([2, 0, 0, 0]) + b"action|log\nmsg|xd\n")

    packet = growtopia.TextPacket("action|log\nmsg|xd\n")
    assert (data:=packet.pack()) and data == (bytearray([2, 0, 0, 0]) + b"action|log\nmsg|xd\n")

    packet = growtopia.MsgPacket("action|log\nmsg|xd\n")
    assert (data:=packet.pack()) and data == (bytearray([3, 0, 0, 0]) + b"action|log\nmsg|xd\n")

if __name__ == "__main__":
    test_protocol()
