"""Test the protocol package."""

import pytest

from growtopia import (
    ErrorManager,
    PacketTooSmall,
    PacketTypeDoesNotMatchContent,
    protocol,
)

ErrorManager.catch_exceptions = False


def test_game_update_packet() -> None:
    """Test the GameUpdatePacket class"""
    packet = protocol.GameUpdatePacket(
        update_type=protocol.GameUpdatePacketType.CALL_FUNCTION,
        variant_list=protocol.VariantList("OnConsoleMessage", "Hello World!"),
    )

    assert packet.flags == protocol.GameUpdatePacketFlags.EXTRA_DATA

    assert packet.extra_data_size == 41
    assert packet.extra_data == b"\x02\x00\x02\x10\x00\x00\x00OnConsoleMessage\x01\x02\x0c\x00\x00\x00Hello World!"

    assert (
        packet.serialise()
        == b"\x04\x00\x00\x00\x01\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00)\x00\x00\x00\x02\x00\x02\x10\x00\x00\x00OnConsoleMessage\x01\x02\x0c\x00\x00\x00Hello World!"
    )

    from_bytes_packet = protocol.GameUpdatePacket.from_bytes(packet.serialise())

    assert from_bytes_packet._type == protocol.PacketType.GAME_UPDATE
    assert from_bytes_packet.update_type == protocol.GameUpdatePacketType.CALL_FUNCTION
    assert from_bytes_packet.flags == protocol.GameUpdatePacketFlags.EXTRA_DATA

    assert from_bytes_packet.extra_data_size == 41
    assert (
        from_bytes_packet.extra_data
        == b"\x02\x00\x02\x10\x00\x00\x00OnConsoleMessage\x01\x02\x0c\x00\x00\x00Hello World!"
    )


def test_text_packet() -> None:
    """Test the text packet class"""
    packet = protocol.TextPacket("Hello, world!")

    assert packet._type == protocol.PacketType.TEXT
    assert packet.text == "Hello, world!"

    packet.text += "\nHello, world!\n"

    assert packet.text == "Hello, world!\nHello, world!\n"

    packet = protocol.TextPacket.from_bytes(packet.serialise())

    assert packet._type == protocol.PacketType.TEXT
    assert (
        packet.text == "Hello, world!\nHello, world!"
    )  # without the last \n because we remove it in the deserialise function

    packet = protocol.TextPacket()
    packet.text = "tankIDName|.\ntankIDPass|.\nrequestedName|.\n"

    packet = protocol.TextPacket.from_bytes(packet.serialise())

    assert packet._type == protocol.PacketType.TEXT
    assert packet.kvps == {
        "tankIDName": ".",
        "tankIDPass": ".",
        "requestedName": ".",
    }

    with pytest.raises(PacketTypeDoesNotMatchContent):
        protocol.TextPacket.from_bytes(protocol.GameUpdatePacket().serialise())

    with pytest.raises(PacketTooSmall):
        protocol.TextPacket.from_bytes(b"b")


if __name__ == "__main__":
    test_game_update_packet()
    test_text_packet()
