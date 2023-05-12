"""Test the protocol package."""

import pytest
from growtopia import (
    protocol,
    ErrorManager,
    PacketTypeDoesNotMatchContent,
    PacketTooSmall,
)


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

    ErrorManager.catch_exceptions = False

    with pytest.raises(PacketTypeDoesNotMatchContent):
        protocol.TextPacket(protocol.GameMessagePacket().serialise())

    with pytest.raises(PacketTooSmall):
        protocol.TextPacket(
            b"b"
        ).deserialise()  # call the deserialise method manually since we don't call it when we instantiate a packet with data with length < 4


if __name__ == "__main__":
    test_packet()
    test_text_packet()
