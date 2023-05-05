"""Test the protocol package."""

from growtopia import protocol


def test_packet() -> None:
    """Test the packet class"""


def test_text_packet() -> None:
    """Test the text packet class"""
    packet = protocol.TextPacket()
    packet.text = "Hello, world!"

    assert packet.type == protocol.PacketType.TEXT
    assert packet.text == "Hello, world!"

    packet.text += "\nHello, world!\n"

    assert packet.text == "Hello, world!\nHello, world!\n"

    packet = protocol.TextPacket(packet.serialise())

    assert packet.type == protocol.PacketType.TEXT
    assert (
        packet.text == "Hello, world!\nHello, world!"
    )  # without the last \n because we remove it in the deserialise function

    packet = protocol.TextPacket()
    packet.text = "tankIDName|.\ntankIDPass|.\nrequestedName|.\n"

    packet = protocol.TextPacket(packet.serialise())

    assert packet.type == protocol.PacketType.TEXT
    assert packet.kvps == {
        "tankIDName": ".",
        "tankIDPass": ".",
        "requestedName": ".",
    }


if __name__ == "__main__":
    test_packet()
    test_text_packet()
