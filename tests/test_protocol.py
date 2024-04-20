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
    assert packet.get_mapping() == {"action": "log", "msg": "xd"}

    packet = growtopia.UpdatePacket(int_y=1)
    assert (data:=packet.pack()) and data == bytearray(b'\x04\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00') and len(data) == 56

if __name__ == "__main__":
    test_protocol()
