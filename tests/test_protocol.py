"""Test the protocol package."""

from growtopia import protocol


def test_packet() -> None:
    """Test the packet class"""


def test_text_packet() -> None:
    """Test the text packet class"""
    packet = protocol.TextPacket()
    packet.set_text("Hello, world!")

    assert packet.type == protocol.PacketType.TEXT
    assert packet.text == "Hello, world!\n"

    packet.append_text("\nHello, world!")

    assert packet.text == "Hello, world!\nHello, world!\n"


if __name__ == "__main__":
    test_packet()
    test_text_packet()
