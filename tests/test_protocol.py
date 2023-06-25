"""Test the protocol package."""

import pytest

from growtopia import ErrorManager, PacketTooSmall, PacketTypeDoesNotMatchContent, protocol


def test_game_update_packet() -> None:
    """Test the GameUpdatePacket class"""
    packet = protocol.GameUpdatePacket()
    packet.update_type = protocol.GameUpdatePacketType.CALL_FUNCTION

    variant_list = protocol.VariantList("OnConsoleMessage")
    variant_list.append(protocol.Variant("Hello World!"))

    packet.set_variant_list(variant_list)

    assert packet.flags == protocol.GameUpdatePacketFlags.EXTRA_DATA

    assert packet.extra_data_size == 41
    assert packet.extra_data == b"\x02\x00\x02\x10\x00\x00\x00OnConsoleMessage\x01\x02\x0c\x00\x00\x00Hello World!"

    assert (
        packet.serialise()
        == b"\x04\x00\x00\x00\x01\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00)\x00\x00\x00\x02\x00\x02\x10\x00\x00\x00OnConsoleMessage\x01\x02\x0c\x00\x00\x00Hello World!"
    )

    from_bytes_packet = protocol.GameUpdatePacket(packet.serialise())

    assert from_bytes_packet.type == protocol.PacketType.GAME_UPDATE
    assert from_bytes_packet.update_type == protocol.GameUpdatePacketType.CALL_FUNCTION
    assert from_bytes_packet.flags == protocol.GameUpdatePacketFlags.EXTRA_DATA

    assert from_bytes_packet.extra_data_size == 41
    assert (
        from_bytes_packet.extra_data
        == b"\x02\x00\x02\x10\x00\x00\x00OnConsoleMessage\x01\x02\x0c\x00\x00\x00Hello World!"
    )


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
    test_game_update_packet()
    test_text_packet()
